from flask import Blueprint, render_template, request, session
from app.services.ai_service import AIService

main = Blueprint("main", __name__)
ai_service = AIService()


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/pdf-chat", methods=["GET", "POST"])
def pdf_chat():

    # Initialize chat history
    if "chat_history" not in session:
        session["chat_history"] = []
    # FIX old session format automatically
    elif isinstance(session["chat_history"][0], str):
        session["chat_history"] = []


    if request.method == "POST":
        user_message = request.form.get("user_input")

        # Store user message (structured format)
        session["chat_history"].append({
            "role": "user",
            "content": user_message
        })

        # ✅ LIMIT MEMORY (important for TinyLlama)
        session["chat_history"] = session["chat_history"][-6:]

        # Generate AI reply
        ai_reply = ai_service.generate_response(session["chat_history"])

        # Store AI reply
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
