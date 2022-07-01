from marshmallow import Schema, fields

class ClassroomSchema(Schema):
  classroom = fields.Str()
