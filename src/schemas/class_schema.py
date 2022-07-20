from dataclasses import field
from marshmallow import Schema, fields

class ClassOccurrenceSchema(Schema):
  schedule = fields.Str()
  # classroom = fields.Str()


class ClassSchema(Schema):
  class_code = fields.Str()
  subject_code = fields.Str()
  subject_name = fields.Str()
  professor = fields.Str()
  start_period = fields.Date()
  end_period = fields.Date()
  occurrences = fields.List(fields.Nested(ClassOccurrenceSchema))
  vacancies = fields.Int()
  subscribers = fields.Int()