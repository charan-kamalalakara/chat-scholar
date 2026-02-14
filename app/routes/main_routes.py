import os
from flask import Blueprint, render_template, request, session
from app.services.ai_service import AIService
from app.utils.pdf_reader import extract_text_from_pdf

main = Blueprint("main", __name__)
ai_service = AIService()


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/clear-chat")
def clear_chat():
    session.pop("chat_history", None)
    return render_template("pdf_chat.html", chat_history=[])


@main.route("/pdf-chat", methods=["GET", "POST"])
def pdf_chat():

    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":

        # -------- PDF Upload --------
        if "pdf_file" in request.files:
            pdf = request.files["pdf_file"]

            if pdf and pdf.filename.endswith(".pdf"):
                os.makedirs("data", exist_ok=True)
                save_path = os.path.join("data", pdf.filename)
                pdf.save(save_path)

                print(f"PDF saved at: {save_path}")

                # ✅ Extract text
                pdf_text = extract_text_from_pdf(save_path)

                # Store document text in session
                session["document_text"] = pdf_text

                print("PDF text extracted successfully")

        # -------- Chat Message --------
        user_message = request.form.get("user_input")

        if user_message:
            session["chat_history"].append({
                "role": "user",
                "content": user_message
            })

            session["chat_history"] = session["chat_history"][-6:]

            document_text = session.get("document_text")

            ai_reply = ai_service.generate_response(
                session["chat_history"],
                document_text=document_text
            )


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
