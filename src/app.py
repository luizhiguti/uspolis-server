from flask import Flask
from flask_cors import CORS

from src.blueprints.classroom_blueprint import classroom_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(classroom_blueprint)
