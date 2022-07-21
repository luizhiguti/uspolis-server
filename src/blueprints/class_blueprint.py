from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import EXCLUDE

from src.common.database import database
from src.common.crawler import get_jupiter_class_infos
from src.schemas.class_schema import ClassSchema

class_blueprint = Blueprint("classes", __name__, url_prefix="/api/classes")

classes = database["classes"]
classes.create_index("class_code", unique=True)

class_schema = ClassSchema(unknown=EXCLUDE)

@class_blueprint.route("many", methods=["POST"])
def create_many_classes():
  subject_codes_list = request.json
  classes_list = []

  for subject_code in subject_codes_list:
    subject_classes = get_jupiter_class_infos(subject_code)

    for class_info in subject_classes:
      schema_load = class_schema.load(class_info)
      classes_list.append(schema_load)

  result = classes.insert_many(classes_list)

  return dumps(result.inserted_ids)