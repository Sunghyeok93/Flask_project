from pyArango.collection import Collection, Field, Edges
import pyArango.validation as VAL
from . import validation

# 유저간의 연결을 담당하는  friend 도큐먼트(edge)
class Friends(Edges):
    _fields = {
        'friend': Field(validators=[VAL.NotNull(), validation.Boolean_val()])
    }