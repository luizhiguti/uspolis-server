from marshmallow import Schema, fields

class ClassroomSchema(Schema):
  classroom_name = fields.Str()
  building = fields.Int()
  floor = fields.Str()
  capacity = fields.Int()
  air_conditioning = fields.Bool()
  projector = fields.Bool()
  accessibility = fields.Bool()
  created_at = fields.DateTime()
  updated_at = fields.DateTime()
