from flask import Blueprint, Flask, jsonify

app = Flask(__name__)
classrom_blueprint = Blueprint('classroom', __name__)

@classrom_blueprint.route('/all-classrooms')
def get_all_classroms():
  return jsonify([
    {
      "name" : "C1-30 "
    },
    {
      "name" : "A1"
    }
  ])
