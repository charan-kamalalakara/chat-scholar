from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/pdf-chat")
def pdf_chat():
    return render_template("pdf_chat.html")

@main.route("/essay-grading")
def essay_grading():
    return render_template("essay_grading.html")
