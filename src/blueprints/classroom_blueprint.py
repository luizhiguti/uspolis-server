from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import ValidationError
from pymongo.errors import DuplicateKeyError, PyMongoError
from datetime import datetime

from src.common.database import database
from src.schemas.classroom_schema import ClassroomSchema

classroom_blueprint = Blueprint("classrooms", __name__, url_prefix="/api/classrooms")

classrooms = database["classrooms"]

# classroom_name not unique
# classrooms.create_index("classroom", unique=True)

classroom_schema = ClassroomSchema()

@classroom_blueprint.route("")
def get_all_classrooms():
  result = classrooms.find({}, { "_id" : 0 })
  resultList = list(result)

  return dumps(resultList)


@classroom_blueprint.route("", methods=["POST"])
def create_classroom():
  try:
    classroom_schema.load(request.json)
    dict_request_body = request.json

    dict_request_body['updated_at'] = datetime.now().strftime("%d/%m%Y %H:%M")

    result = classrooms.insert_one(dict_request_body)

    return dumps(result.inserted_id)

  except DuplicateKeyError as err:
    return { "message" : err.details["errmsg"] }, 400

  except ValidationError as err:
    return { "message" : err.messages }, 400


@classroom_blueprint.route("/<name>", methods=["GET", "DELETE", "PUT"])
def classroom_by_name(name):
  query = { "classroom_name" : name }
  try:
    if request.method == "GET":
      result = classrooms.find_one(query, { "_id" : 0 })

    if request.method == "DELETE":
      result = classrooms.delete_one(query).deleted_count

    if request.method == "PUT":
      classroom_schema.load(request.json)
      dict_request_body = request.json
      dict_request_body['updated_at'] = datetime.now().strftime("%d/%m%Y %H:%M")

      update_set = {"$set" : dict_request_body }
      result = classrooms.update_one(query, update_set).modified_count

    if not result: raise PyMongoError(f"{name} not found")

    return dumps(result)

  except ValidationError as err:
    return { "message" : err.messages }, 400

  except PyMongoError as err:
    return { "message" : err._message }
