from marshmallow import Schema, fields

from src.schemas.class_schema import PreferencesSchema

class EventSchema(Schema):
  class_code = fields.Str()
  subject_code = fields.Str()
  subject_name = fields.Str()
  professor = fields.Str()
  start_period = fields.Str()
  end_period = fields.Str()
  start_time = fields.Str()
  end_time = fields.Str()
  week_day = fields.Str()
  class_type = fields.Str()
  vacancies = fields.Int()
  subscribers = fields.Int()
  pendings = fields.Int()
  preferences = fields.Nested(PreferencesSchema)
  classroom = fields.Str()
  building = fields.Str()