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

@blueprint.route('/removeRelation', methods=['post'])
def removeRelation():
    arango.removeRelation('Members','197796')
    return "removeRelation"

@blueprint.route('/addUser', methods=["POST"])
def addUser():
    json = request.form
    userName = json['data[name]']
    arango.addVertex('Users', { "_key" : userName })
    return "True"

@blueprint.route('/addFriend', methods=["POST"])
def addFriend():
    json = request.form
    userName1 = json['data[name1]']
    userName2 = json['data[name2]']
    arango.addRelation('Friends','Users', userName1, 'Users', userName2, { "_key" : userName1+userName2} )
    return "True"

@blueprint.route('/addProject', methods=["POST"])
def addProject():
    json = request.form
    projectName = json['data[name]']
    arango.addVertex('Projects', { "_key" : projectName })
    return "True"

@blueprint.route('/addAuthor', methods=["POST"])
def addAuthor():
    json = request.form
    projectName = json['data[project]']
    userName = json['data[user]']
    author = json['data[author]']
    arango.addRelation('Members', 'Users', userName, 'Projects', projectName, {"_key":userName+projectName, "position":author})
    return "True"

# ralation에 대한 _key Attribute 네이밍 정하기