import pyArango.validation as VAL
from pyArango.theExceptions import ValidationError
import types

class String_val(VAL.Validator):
 def validate(self, value):
     if type(value) is not str :
         raise ValidationError("Field value must be a String")
     return True

class Int_val(VAL.Validator):
 def validate(self, value):
     if type(value) is not int :
         raise ValidationError("Field value must be a Integer")
     return True

class Position_val(VAL.Validator) :
    def validate(self, value):
        if value is not "Owner" or 'Participant' :
            raise ValidationError("Field value must be a Owner/Participant")
        return True

class Boolean_val(VAL.Validator) :
    def validate(self, value):
        if value is not True or False :
            raise ValidationError("Field value must be a Boolean")
        return True
