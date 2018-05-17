import pyArango.collection as COL
import pyArango.validation as VAL

class Tasks(COL.Collection):
    _validation = {
        'on_save': False,
        'on_set': False,
        'allow_foreign_fields': True
    }
    _fields = {
        'name': COL.Field(validators=[VAL.NotNull()]),
    }



