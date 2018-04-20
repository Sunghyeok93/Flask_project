from pyArango.collection import Collection, Field, Edges
import pyArango.validation as VAL
from . import validation

# 유저와 프로젝트간의 연결을 담당하는 멤버 도큐먼트(edge)
class Members(Edges):

    _fields = {
        'joinDate': Field(validators=[VAL.NotNull(), validation.String_val()]),
        'position': Field(validators=[VAL.NotNull()])
    }