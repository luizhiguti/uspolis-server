from flask import Flask
from flask_cors import CORS

from src.blueprints.classroom_blueprint import classroom_blueprint
from src.blueprints.class_blueprint import class_blueprint
from src.blueprints.subject_blueprint import subject_blueprint
from src.blueprints.allocation_blueprint import allocation_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(classroom_blueprint)
app.register_blueprint(class_blueprint)
app.register_blueprint(subject_blueprint)
app.register_blueprint(allocation_blueprint)
