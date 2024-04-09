from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return 'Hello from Flask!'


from book_library_app import authors