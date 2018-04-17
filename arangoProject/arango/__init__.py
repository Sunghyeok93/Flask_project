from flask import Blueprint, request, render_template
from arango.model.users import *
from . import collection, connection

blueprint = Blueprint('_arango', __name__)
arango = connection.arangoConnect()

@blueprint.route('/')
def hello_world():
    return render_template('main.html')


@blueprint.route('/addVertex', methods=["POST"])
def addVertex():
    arango.addVertex('Users', { "name" : "111", "_key" : "newKey", "e":"e" } )
    return "addVertex"


@blueprint.route('/addRelation', methods=['post'])
def addRelation():
    _fromVertex = {"name":"from", "_key" : "from"}
    _toVertex = {"name": "to", "_key": "to"}
    arango.removeVertex('Users', "from")
    arango.removeVertex('Groups', "to")
    arango.addVertex('Users', _fromVertex)
    arango.addVertex('Groups', _toVertex)
    arango.addRelation('Members', 'Users', 'from', 'Groups', 'to', {"hello":"man"})
    return "addRelation"
