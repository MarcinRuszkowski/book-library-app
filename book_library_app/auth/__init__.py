from flask import Blueprint


auth_bp = Blueprint('auht', __name__)

from book_library_app.auth import auth