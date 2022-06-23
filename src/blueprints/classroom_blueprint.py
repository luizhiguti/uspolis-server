from flask import Blueprint, request
from bson.json_util import dumps

from src.common.database import database

classroom_blueprint = Blueprint("classrooms", __name__, url_prefix="/api/classrooms")

classrooms = database["classrooms"]

@classroom_blueprint.route("")
def get_classroom():
  result = classrooms.find()
  resultList = list(result)

  return dumps(resultList)

@classroom_blueprint.route("", methods=["POST"])
def create_classroom():

  dict_request_body = request.json

  result = classrooms.insert_one(dict_request_body)

  return dumps(result.inserted_id)

@classroom_blueprint.route("/<name>", methods=["GET", "DELETE", "PUT"])
def get_classroom_by_name(name):
  query = { "name" : name }

  if request.method == "GET":
    result = classrooms.find_one(query)

  if request.method == "DELETE":
    result = classrooms.delete_one(query).raw_result

  if request.method == "PUT":
    update_set = {"$set" : request.json }
    result = classrooms.update_one(query, update_set).raw_result

  return dumps(result)
