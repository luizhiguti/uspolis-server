from marshmallow import Schema, fields

class EventSchema(Schema):
  class_code = fields.Str()
  subject_code = fields.Str()
  week_day = fields.Str()
  start_time = fields.Str()
  end_time = fields.Str()
  classroom = fields.Str()
  building = fields.Str()

class AllocationSchema(EventSchema):
  start_period = fields.Str()
  end_period = fields.Str()
  professor = fields.Str()