from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = Flask(__name__)
cors = CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"expire_on_commit": False})
api = Api(app)