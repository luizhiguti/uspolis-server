from flask import Flask
from flask_restful import Api

from src.blueprints.classrom_blueprint import classrom_blueprint

app = Flask(__name__)
api = Api(app)

app.register_blueprint(classrom_blueprint)
