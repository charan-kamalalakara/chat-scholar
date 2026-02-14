from flask import Blueprint

# Create a Blueprint
main = Blueprint("main", __name__)

# Home route
@main.route("/")
def home():
    return "Chat Scholar backend is running!"
