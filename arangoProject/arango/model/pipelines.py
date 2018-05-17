import pyArango.collection as COL
import pyArango.validation as VAL

class Pipelines(COL.Collection):
    _validation = {
        'on_save': False,
        'on_set': False,
        'allow_foreign_fields': True
    }
    _fields = {
        'name': COL.Field(validators=[VAL.NotNull()]),
        'owner': COL.Field(validators=[VAL.NotNull()]),
        'url': COL.Field(validators=[VAL.NotNull()]),
        'format': COL.Field(validators=[VAL.NotNull()]),
        'data': COL.Field(validators=[VAL.NotNull()])
    }



