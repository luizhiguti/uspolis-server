from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import EXCLUDE
from pymongo.errors import PyMongoError


from src.common.database import database
from src.common.crawler import get_jupiter_class_infos
from src.schemas.class_schema import ClassSchema, PreferencesSchema

class_blueprint = Blueprint("classes", __name__, url_prefix="/api/classes")

classes = database["classes"]

# USING UPSERT
# classes.create_index({ "class_code" : 1, "subject_code" : 1 }, unique=True)

class_schema = ClassSchema(unknown=EXCLUDE)
preferences_schema = PreferencesSchema(unknown=EXCLUDE)


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
      print(subject_classes)

      for class_info in subject_classes:
        schema_load = class_schema.load(class_info)

        query = { "class_code" : schema_load["class_code"], "subject_code" : schema_load["subject_code"] }
        result = classes.update_one(query, { "$set" : schema_load }, upsert=True)

        updated.append(schema_load["subject_code"]) if result.matched_count else inserted.append(schema_load["subject_code"])

    return dumps({ "updated" : updated, "inserted" : inserted })

  except Exception as ex:
    print(ex)
    return { "message" : f"Erro ao buscar informações das turmas - {subject_code}", "updated" : updated, "inserted" : inserted }, 400

@class_blueprint.route("/<subject_code>/<class_code>", methods=["DELETE"])
def delete_by_subject_class_code(subject_code, class_code):
  query = { "subject_code" : subject_code, "class_code" : class_code }
  try:
    result = classes.delete_one(query).deleted_count
    if not result: raise PyMongoError(f"{subject_code} - {class_code} not found")
    return dumps(result)

  except PyMongoError as err:
    return { "message" : err._message }

@class_blueprint.route("/<subject_code>/<class_code>", methods=["PATCH"])
def update_preferences(subject_code, class_code):
  query = { "subject_code" : subject_code, "class_code" : class_code }
  try:
    schema_load = preferences_schema.load(request.json)
    result = classes.update_one(query, { "$set" : { "preferences": schema_load } })

    return dumps(result.modified_count)

  except PyMongoError as err:
    return { "message" : err._message }

@class_blueprint.route("/<subject_code>/<class_code>", methods=["GET"])
def get_preferences(subject_code, class_code):
  query = { "subject_code" : subject_code, "class_code" : class_code }
  try:
    result = classes.find_one(query, { "_id" : 0 })

    if not result: raise PyMongoError(f"{subject_code}/{class_code} not found")

    return dumps(result)

  except PyMongoError as err:
    return { "message" : err._message }