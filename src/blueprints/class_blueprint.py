from flask import Blueprint, request
from bson.json_util import dumps

from src.common.database import database
from src.schemas.class_schema import ClassSchema

class_blueprint = Blueprint("classes", __name__, url_prefix="/api/classes")

classes = database["classes"]

classSchema = ClassSchema()

@class_blueprint.route("many", methods=["POST"])
def create_many_classes():
  subject_codes_list = request.json
  classes_list = []

  for subject_code in subject_codes_list:
    print(subject_code)
    subject_classes = [{ "subject_code" : subject_code }] # crawler
    classes_list += subject_classes

  result = classes.insert_many(classes_list)

  return dumps(result.inserted_ids)