from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import EXCLUDE

from src.common.database import database
from src.common.crawler import get_jupiter_class_infos
from src.schemas.class_schema import ClassSchema

class_blueprint = Blueprint("classes", __name__, url_prefix="/api/classes")

classes = database["classes"]

# USING UPSERT
# classes.create_index({ "class_code" : 1, "subject_code" : 1 }, unique=True)

class_schema = ClassSchema(unknown=EXCLUDE)


@class_blueprint.route("", methods=["GET"])
def get_all_classes():
  result = classes.find({}, { "_id" : 0 })
  resultList = list(result)

  return dumps(resultList)


@class_blueprint.route("many", methods=["POST"])
def create_many_classes():
  try:
    subject_codes_list = request.json
    updated = []
    inserted = []

    for subject_code in subject_codes_list:
      subject_classes = get_jupiter_class_infos(subject_code)

      for class_info in subject_classes:
        schema_load = class_schema.load(class_info)

        query = { "class_code" : schema_load["class_code"], "subject_code" : schema_load["subject_code"] }
        result = classes.update_one(query, { "$set" : schema_load }, upsert=True)

        updated.append(schema_load["subject_code"]) if result.matched_count else inserted.append(schema_load["subject_code"])

    return dumps({ "updated" : updated, "inserted" : inserted })

  except:
    return { "message" : f"Erro ao buscar informações das turmas - {subject_code}", "updated" : updated, "inserted" : inserted }, 400
