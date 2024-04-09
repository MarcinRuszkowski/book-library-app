from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

with app.app_context():
    result = db.session.execute(text('show tables;'))

for row in result:
    print(row)


from book_library_app import authors