from marshmallow import Schema, fields

class ClassroomSchema(Schema):
  classroom_name = fields.Str()
  building = fields.Str()
  floor = fields.Int()
  capacity = fields.Int()
  air_conditioning = fields.Bool()
  projector = fields.Bool()
  accessibility = fields.Bool()
  updated_at = fields.Str()

class AvailableClassroomsQuerySchema(Schema):
  week_day = fields.Str(required=True)
  start_time = fields.Str(required=True)
  end_time = fields.Str(required=True)
