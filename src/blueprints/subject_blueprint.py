from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import ValidationError
from pymongo.errors import DuplicateKeyError, PyMongoError

from src.common.database import database
from src.schemas.subject_schema import SubjectSchema

subject_blueprint = Blueprint("subjects", __name__, url_prefix="/api/subjects")

subjects = database["subjects"]
subjects.create_index("subject_code", unique=True)

subject_schema = SubjectSchema()

@subject_blueprint.route("", methods=["GET"])
def get_all_subjects():
  result = subjects.find({}, { "_id" : 0 })
  resultList = list(result)

  return dumps(resultList)

@subject_blueprint.route("", methods=["POST"])
def create_subject():
  try:
    dict_request_body = request.json
    subject_schema.load(dict_request_body)

    result = subjects.insert_one(dict_request_body)

    return dumps(result.inserted_id)

  except DuplicateKeyError as err:
    return { "message" : err.details["errmsg"] }, 400

  except ValidationError as err:
    return { "message" : err.messages }, 400

@subject_blueprint.route("<code>", methods=["DELETE"])
def delete_subject(code):
  query = { "subject_code" : code }
  try:
    result = subjects.delete_one(query).deleted_count

    if not result: raise PyMongoError(f"{code} not found")

  except PyMongoError as err:
    return { "message" : err._message }, 400