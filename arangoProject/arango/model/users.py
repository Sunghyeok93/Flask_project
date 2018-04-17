import pyArango.collection as COL
import pyArango.validation as VAL
from . import validation

# 유저 정보를 담을 도큐먼트용 컬렉션(Vertex)
class Users(COL.Collection):
    _validation = {
        'on_save': False,
        'on_set': False,
        'allow_foreign_fields': True
    }

    _fields = {
        'name': COL.Field(validators=[VAL.NotNull(), validation.String_val()]),
        'email': COL.Field(validators=[VAL.NotNull()]),
        'password': COL.Field(validators=[VAL.NotNull()]),
    }



