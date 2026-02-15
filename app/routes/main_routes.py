import os
from flask import Blueprint, render_template, request, session

from app.services.ai_service import AIService
from app.services.embedding_service import EmbeddingService

from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.text_chunker import split_text_into_chunks
from app.utils.vector_store import VectorStore


main = Blueprint("main", __name__)

# Services
ai_service = AIService()
embedding_service = EmbeddingService()

# Global vector DB (in-memory)
vector_store = VectorStore.load()



@main.route("/")
def home():
    return render_template("home.html")


@main.route("/clear-chat")
def clear_chat():
    session.pop("chat_history", None)
    return render_template("pdf_chat.html", chat_history=[])


@main.route("/pdf-chat", methods=["GET", "POST"])
def pdf_chat():

    global vector_store

    # Initialize chat history
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":

        # =========================
        # PDF UPLOAD HANDLING
        # =========================
        if "pdf_file" in request.files:
            pdf = request.files["pdf_file"]

            if pdf and pdf.filename.endswith(".pdf"):

                os.makedirs("data", exist_ok=True)
                save_path = os.path.join("data", pdf.filename)
                pdf.save(save_path)

                print(f"PDF saved at: {save_path}")

                # Extract text
                pdf_text = extract_text_from_pdf(save_path)

                # Create chunks
                chunks = split_text_into_chunks(pdf_text)

                print(f"Created {len(chunks)} chunks")

                # Generate embeddings
                embeddings = []
                valid_chunks = []

                for chunk in chunks:
                    emb = embedding_service.get_embedding(chunk)
                    if emb:
                        embeddings.append(emb)
                        valid_chunks.append(chunk)

                # Create FAISS vector store
                if embeddings:
                    dimension = len(embeddings[0])
                    vector_store = VectorStore(dimension)
                    vector_store.add_embeddings(
                        embeddings,
                        valid_chunks,
                        source_name=pdf.filename
                    )


                    print("✅ Vector store created successfully")
                    vector_store.save()

        # =========================
        # CHAT MESSAGE HANDLING
        # =========================
        user_message = request.form.get("user_input")

        if user_message:

            # Save user message
            session["chat_history"].append({
                "role": "user",
                "content": user_message
            })

            # Limit memory
            session["chat_history"] = session["chat_history"][-6:]

            retrieved_chunks = None

            # Vector retrieval
            if vector_store:
                query_embedding = embedding_service.get_embedding(user_message)

                if query_embedding:
                    retrieved_chunks = vector_store.search(
                        query_embedding,
                        top_k=3
                    )

            # Generate AI response
            ai_reply = ai_service.generate_response(
                session["chat_history"],
                document_chunks=retrieved_chunks
            )

            # Save AI response
            session["chat_history"].append({
                "role": "assistant",
                "content": ai_reply
            })

            session.modified = True

    return render_template(
        "pdf_chat.html",
        chat_history=session["chat_history"]
    )


@main.route("/essay-grading")
def essay_grading():
    return render_template("essay_grading.html")
