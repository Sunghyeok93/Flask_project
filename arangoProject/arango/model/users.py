from pyArango.collection import Edges
import pyArango.collection as COL
import pyArango.validation as VAL
from . import validation
from pyArango.theExceptions import ValidationError
import types


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
        'species': COL.Field(validators=[VAL.NotNull(), VAL.Length(5, 15), validation.String_val()])
    }

class Member(Edges):

    _validation = {
        'on_save': False,
        'on_set': False,
        'allow_foreign_fields': True # allow fields that are not part of the schema
    }

    _fields = {
        'joinDate': COL.Field(validators=[VAL.NotNull(), validation.String_val()]),
        'position': COL.Field(validators=[VAL.NotNull(), validation.String_val()])
    }