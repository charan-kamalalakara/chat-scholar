from flask import Blueprint, render_template, request
from app.services.ai_service import AIService

main = Blueprint("main", __name__)
ai_service = AIService()

@main.route("/")
def home():
    return render_template("home.html")


@main.route("/pdf-chat", methods=["GET", "POST"])
def pdf_chat():
    response = None
    user_message = None

    if request.method == "POST":
        user_message = request.form.get("user_input")
        response = ai_service.generate_response(user_message)

    return render_template(
        "pdf_chat.html",
        response=response,
        user_message=user_message
    )


@main.route("/essay-grading")
def essay_grading():
    return render_template("essay_grading.html")
