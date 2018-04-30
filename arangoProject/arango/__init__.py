from flask import Blueprint, request, render_template, jsonify, session, json, Response
from arango.model.users import *
from . import connection, dbResponse

blueprint = Blueprint('_arango', __name__)
arango = connection.arangoConnect()
dbresponse = dbResponse.arangoResponse()

@blueprint.route('/')
def hello_world():
    return render_template('main.html')

# 세션 생성 성공시 status 200, 새션 성공 실패(이미 세션 존재) status 404 리턴
@blueprint.route('/addSession', methods=["POST"])
def setSession():
    json = request.form
    session_id = json['data[email]']
    if not 'ID' in session :
        session['ID'] = session_id
        return dbresponse.statusResponse(responseStatus=200)
    else :
        print(session['ID'])
        return dbresponse.statusResponse(responseStatus=404)


# 성공적으로 세션 해제시 status 200, 세션 해제 실패(세션이 이미 존재하지않음) status 404 리턴
@blueprint.route('/deleteSession', methods=["POST"])
def deleteSession():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=404)
    else :
        print(session['ID'])
        del session['ID']
        return dbresponse.statusResponse(responseStatus=200)

@blueprint.route('/create/user', methods=["POST"])
def createUser():
    if not 'ID' in session :
        return Response(status=401)
    else :
        json = request.form
        email = json['data[email]']
        name = json['data[name]']
        pwd = json['data[pwd]']
        desc = json['data[desc]']
        arango.addVertex('Users', {"_key": "Yuha", "name": name, "pwd": pwd, "desc": desc})
        print('1111')
        if arango.addVertex('Users', {"_key": "Yuha", "name": name, "pwd" : pwd, "desc" : desc}) :
            return Response(status=200)
        else :
            return Response(status=404)



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
    result = arango.addVertex('Users', { "_key" : userName })

    if result == False :
        return jsonify(addUser=False, username=userName)
    else :
        return jsonify(addUser=True, username=userName)

@blueprint.route('/returnFriends', methods=["POST"])
def returnFriends():
    json = request.form
    userName = json['data[name]']
    #result = arango.returnVertex('Users', userName)
    result = arango.getEdges('Users', 'in', 'Yuha')
    if result == False :
        return jsonify(returnFriends=False, username=userName)
    else :
        return jsonify(returnFriends=False, username=userName)

@blueprint.route('/addFriend', methods=["POST"])
def addFriend():
    json = request.form
    userName1 = json['data[name1]']
    userName2 = json['data[name2]']
    result = arango.addRelation('Friends','Users', userName1, 'Users', userName2, { "_key" : userName1+userName2} )

    if result == False :
        return jsonify(addFriend=False, username1=userName1, username2=userName2)
    else :
        return jsonify(addFriend=True, username1=userName1, username2=userName2)

@blueprint.route('/addProject', methods=["POST"])
def addProject():
    json = request.form
    projectName = json['data[name]']
    result = arango.addVertex('Projects', { "_key" : projectName })

    if result == False:
        return jsonify(addProject=False, projectname=projectName)
    else:
        return jsonify(addProject=True, username=projectName)

@blueprint.route('/joinProject', methods=["POST"])
def joinProject():
    json = request.form
    projectName = json['data[project]']
    userName = json['data[user]']
    author = json['data[author]']
    result = arango.addRelation('Members', 'Users', userName, 'Projects', projectName, {"_key":userName+projectName, "position":author})

    if result == False:
        return jsonify(joinProject=False, projectname=projectName,username = userName, author=author)
    else:
        return jsonify(joinProject=True, projectname=projectName, username=userName, author=author)




# ralation에 대한 _key Attribute 네이밍 정하기
# hasUser, hasProject, 내 친구들, 내 프로젝트