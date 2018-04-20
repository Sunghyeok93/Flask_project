import pyArango.collection as COL
import pyArango.validation as VAL
from . import validation

# 그룹 정보를 담을 도큐먼트용 컬렉션(Vertex)
class Projects(COL.Collection):
    _validation = {
        'on_save': False,
        'on_set': False,
        'allow_foreign_fields': True
    }

    _fields = {
        'name': COL.Field(validators=[VAL.NotNull(), validation.String_val()]),
        'owner': COL.Field(validators=[VAL.NotNull()]),
    }

