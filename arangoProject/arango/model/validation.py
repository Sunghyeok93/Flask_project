import pyArango.validation as VAL
from pyArango.theExceptions import ValidationError
import types

class String_val(VAL.Validator):
 def validate(self, value):
     if type(value) is not str :
         raise ValidationError("Field value must be a string")
     return True

class Int_val(VAL.Validator):
 def validate(self, value):
     if type(value) is not int :
         raise ValidationError("Field value must be a integer")
     return True
