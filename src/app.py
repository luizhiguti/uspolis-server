from flask import Flask
from flask_restful import Api

from src.blueprints.classroom_blueprint import classroom_blueprint

app = Flask(__name__)
api = Api(app)

app.register_blueprint(classroom_blueprint)
