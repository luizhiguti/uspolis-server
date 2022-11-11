from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import EXCLUDE,INCLUDE, ValidationError

from src.common.database import database
from src.schemas.allocation_schema import AllocatorInputSchema, AllocatorOutputSchema
from src.common.allocation.allocator import allocate_classrooms
from src.common.mappers.classes_mapper import break_class_into_events

event_blueprint = Blueprint("events", __name__, url_prefix="/api/events")

events = database["events"]
classrooms = database["classrooms"]

# class id - class_code, subject_code
# event id - start_time, end_time, week_day
# classroom id - building, classroom

allocation_output_schema = AllocatorOutputSchema()
allocation_input_schema = AllocatorInputSchema(many=True, unknown=EXCLUDE)

@event_blueprint.route("")
def get_events():
  result = events.find({}, { "_id" : 0 })
  resultList = list(result)

  return dumps(resultList)


@event_blueprint.route("allocate", methods=["PATCH"])
def save_allocation():
  try:
    classrooms_list = list(classrooms.find({ "building" : "Biênio" }, { "_id" : 0 }))
    events_list = list(events.find({}, { "_id" : 0 }))

    # parse date & time fields
    allocation_input_schema_load = allocation_input_schema.load(events_list)

    print(f'Number of events: {len(events_list)}')

    allocation_events = allocate_classrooms(classrooms_list, allocation_input_schema_load)
    allocated = 0

    for event in allocation_events:
      allocation_output_schema_load = allocation_output_schema.load(event)
      query = {
        "class_code" : allocation_output_schema_load["class_code"],
        "subject_code" : allocation_output_schema_load["subject_code"],
        "week_day" : allocation_output_schema_load["week_day"]
      }
      result = events.update_one(
        query,
        { "$set" : allocation_output_schema_load },
        upsert=True)

      allocated += result.matched_count

    if allocated != len(events_list):
      raise Exception(f"Matched {allocated} of {len(events_list)} events")

    return ""

  except ValidationError as err:
    return { "message" : err.messages }, 400

  except Exception as ex:
    return { "message" : "Erro ao calcular alocação", "error": str(ex) }, 500


@event_blueprint.route("edit/<subject_code>/<class_code>", methods=["PATCH"])
def edit_allocation(subject_code, class_code):
  try:
    week_days = request.json
    classroom = request.args["classroom"]

    query = {
        "subject_code" : subject_code,
        "class_code" : class_code,
        "week_day": { "$in" : week_days }
      }

    result = events.update_many(query,
      { "$set" : { "classroom" : classroom } }
    )

    return dumps(result.matched_count)

  except Exception as ex:
    print(ex)
    return { "message" : ex }, 500
