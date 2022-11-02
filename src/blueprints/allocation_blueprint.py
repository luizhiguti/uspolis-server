from flask import Blueprint, request
from bson.json_util import dumps
from marshmallow import ValidationError

from src.common.database import database
from src.schemas.allocation_schema import EventSchema, AllocationSchema
from src.common.mappers.classes_mapper import break_class_into_events
from src.common.allocation.allocator import allocate_classrooms

allocation_blueprint = Blueprint("allocation", __name__, url_prefix="/api/allocation")

allocation = database["allocation"]
classrooms = database["classrooms"]
classes = database["classes"]

# class id - class_code, subject_code
# event id - start_time, end_time, week_day
# classroom id - building, classroom

event_schema = EventSchema(many=True)

@allocation_blueprint.route("")
def get_allocation():
  result = allocation.find({}, { "_id" : 0 })
  resultList = list(result)

  return dumps(resultList)


@allocation_blueprint.route("", methods=["POST"])
def save_allocation():
# clear allocation collection and save new allocation
  try:
    classrooms_list = list(classrooms.find({ "building" : "Biênio" }, { "_id" : 0 }))
    classes_list = list(classes.find({}, { "_id" : 0 }))
    # set preferences
    for c in classes_list:
      c['preferences'] = {
        'building' : 'Biênio',
        'min_capacity' : False,
        'air_conditioning' : False,
        'projector' : False,
        'accessibility' : False,
      }

    events_list = []

    for c in classes_list:
      events_list += break_class_into_events(c)

    print(f'Number of events: {len(events_list)}')

    allocation_events = allocate_classrooms(classrooms_list, events_list)
    schema_load = event_schema.load(allocation_events)

    allocation.delete_many({})
    result = allocation.insert_many(schema_load)

    if len(result.inserted_ids) != len(events_list):
      raise Exception(f"Inserted {result.inserted_ids} of {events_list} events")

    return ""

  except ValidationError as err:
    return { "message" : err.messages }, 400

  except Exception as ex:
    return { "message" : "Erro ao calcular alocação", "error": ex }, 500