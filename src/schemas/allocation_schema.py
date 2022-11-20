from marshmallow import Schema, fields, post_load

from src.schemas.class_schema import PreferencesSchema

class AllocatorInputSchema(Schema):
  class_code = fields.Str()
  subject_code = fields.Str()
  week_day = fields.Str()
  start_time = fields.Time("%H:%M")
  end_time = fields.Time("%H:%M")
  subscribers = fields.Int()
  preferences = fields.Nested(PreferencesSchema)

  @post_load
  def create_ids(self, data, **_):
    data["event_id"] = data["subject_code"] + "_" + data["class_code"] + "_" + data["week_day"]
    data["class_id"] = data["subject_code"] + "_" + data["class_code"]
    return data


class AllocatorOutputSchema(Schema):
  class_code = fields.Str()
  subject_code = fields.Str()
  week_day = fields.Str()
  start_time = fields.Str()
  end_time = fields.Str()
  classroom = fields.Str()
  building = fields.Str()