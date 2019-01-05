from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY='SOME RANDOM SECRET KEY__!#(*&WERKL',
    SQLALCHEMY_DATABASE_URI='sqlite:///bingo.sqlite3',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)
