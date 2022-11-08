from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import EXCLUDE,INCLUDE, ValidationError

from src.common.database import database
from src.schemas.event_schema import EventSchema
from src.schemas.allocation_schema import AllocatorInputSchema, AllocatorOutputSchema
from src.common.allocation.allocator import allocate_classrooms
from src.common.mappers.classes_mapper import break_class_into_events

event_blueprint = Blueprint("events", __name__, url_prefix="/api/events")

events = database["events"]
classrooms = database["classrooms"]

# class id - class_code, subject_code
# event id - start_time, end_time, week_day
# classroom id - building, classroom

event_schema = EventSchema(unknown=INCLUDE)
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
    print(allocation_input_schema_load[0])

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

@event_blueprint.route("classes", methods=["PATCH"])
# test classes to events mapper while subject not available in jupiterweb
def test_class_mapper():
  try:
    efc = database['events_from_classes']
    classes = database['classes']

    classes_list = classes.find()

    for c in classes_list:
      # print(c)
      events = break_class_into_events(c)
      for e in events:
        # print(e)
        load = event_schema.load(e)
        query = {
        "class_code" : load["class_code"],
        "subject_code" : load["subject_code"],
        "week_day" : load["week_day"]
        }
        result = efc.update_one(
          query,
          { "$set" : load },
          upsert=True)

    return ""

  except Exception as ex:
    print(ex)
    return "", 500


@event_blueprint.route("parse", methods=["PATCH"])
# parse old allocation to new events data schema
def parse():
  try:
    events_list = events.find()
    parsed = 0

    for e in events_list:
      load = event_schema.load(e)
      query = {
        "class_code" : load["class_code"],
        "subject_code" : load["subject_code"],
        "week_day" : load["week_day"]
      }
      result = events.update_one(
        query,
        { "$set" : load },
        upsert=True)

      parsed += result.matched_count

    return dumps(parsed)

  except Exception as ex:
    print(ex)
    return ""