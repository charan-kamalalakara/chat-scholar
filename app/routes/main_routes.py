from flask import Blueprint, render_template
from app.services.ai_service import AIService

main = Blueprint("main", __name__)
ai_service = AIService()

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/pdf-chat")
def pdf_chat():
    test_response = ai_service.generate_response("Test")
    return render_template("pdf_chat.html", response=test_response)

@main.route("/essay-grading")
def essay_grading():
    return render_template("essay_grading.html")
