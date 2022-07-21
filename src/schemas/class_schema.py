from marshmallow import Schema, fields

class ArraySumField(fields.Field):
  """
  fields to sum array values
  """
  def _deserialize(self, value, attr, data, **kwargs):
    return sum(value)


class ClassSchema(Schema):
  class_code = fields.Str(data_key="cod_turma")
  subject_code = fields.Str(data_key="cod_disciplina")
  subject_name = fields.Str(data_key="nome_disciplina")
  professor = fields.List(fields.Str(), data_key="prof")
  start_period = fields.Str(data_key="inicio")
  end_period = fields.Str(data_key="fim")
  class_type = fields.Str(data_key="tipo")
  vacancies = ArraySumField(data_key="vagass")
  subscribers = ArraySumField(data_key="inscritos")
  pendings = ArraySumField(data_key="pendentess")
