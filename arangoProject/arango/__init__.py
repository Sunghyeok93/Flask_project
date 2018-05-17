from flask import Blueprint, request, render_template, jsonify, session, json, Response
from arango.model.users import *
from . import connection, dbResponse

blueprint = Blueprint('_arango', __name__)
arango = connection.arangoConnect()
dbresponse = dbResponse.arangoResponse()


@blueprint.route('/login')
def login():
    session['ID'] = 'asdasd'
    return render_template('index.html')


@blueprint.route('/')
def hello_world():
    return render_template('main.html')

# 세션 생성 성공시 status 200, 새션 성공 실패(이미 세션 존재) status 401 리턴
@blueprint.route('/addSession', methods=["POST"])
def addSession():
    json = request.form
    session_id = json['data[email]']
    if not 'ID' in session :
        print('connect new session : '+ session_id )
        session['ID'] = session_id
        return dbresponse.statusResponse(responseStatus=200)
    else :
        print('already in session : ' + session['ID'])
        return dbresponse.statusResponse(responseStatus=401)


# 성공적으로 세션 해제시 status 200, 세션 해제 실패(세션이 이미 존재하지않음) status 401 리턴
@blueprint.route('/deleteSession', methods=["POST"])
def deleteSession():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        print(session['ID'])
        session.clear()
        return dbresponse.statusResponse(responseStatus=200)


@blueprint.route('/create/user', methods=["POST"])
def createUser():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        email = json['data[email]']
        name = json['data[name]']
        pwd = json['data[pwd]']
        desc = json['data[desc]']

        if arango.addVertex('Users', {"_key": email, "name": name, "pwd": pwd, "desc": desc}) :
            return dbresponse.statusResponse(responseStatus=200)
        else :
            return dbresponse.statusResponse(responseStatus=400)

@blueprint.route('/confirm/pwd', methods=["POST"])
def confirmPwd():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        pwd = json['data[pwd]']

        if arango.checkAttribute(collection='Users', document=session['ID'], attribute='pwd', checkValue=pwd ) :
            return dbresponse.statusResponse(responseStatus=200)
        else :
            return dbresponse.statusResponse(responseStatus=400)

@blueprint.route('/return/user', methods=["POST"])
def returnUser():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        try :
            document = arango.returnDocument(collection='Users', document=session['ID'])
            return dbresponse.userResponse(email=document['_key'], name=document['name'], pwd=document['pwd'], desc=document['desc'], responseStatus=200)
        except :
            return dbresponse.statusResponse(responseStatus=400)

#미완성 잼 ...
@blueprint.route('/edit/user', methods=["POST"])
def editUser():
    arango.patchDocument(collection='Users', document='sdsdd', jsonValue={})
    return dbresponse.statusResponse(responseStatus=404)

    #if not 'ID' in session :
    #    return dbresponse.statusResponse(responseStatus=401)
    #else :
    #    json = request.form
    #    value = {
    #        'name' : json['data[name]'],
    #        'pwd' : json['data[pwd'],
    #        'desc' : json['data[desc']
    #    }

    #    return dbresponse.statusResponse(responseStatus=404)

@blueprint.route('/delete/user', methods=["POST"])
def deleteUser():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        if arango.removeVertex('Users', session['ID']) :
            del session['ID']
            return dbresponse.statusResponse(responseStatus=200)
        else :
            return dbresponse.statusResponse(responseStatus=400)

@blueprint.route('/send/friend', methods=["POST"])
def sendFriend():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        friendEmail = json['data[email]']

        value = arango.addRelation(edgeCollection='Friends', _fromCollection='Users', _fromVertex=session['ID'], _toCollection='Users', _toVertex=friendEmail, content={"_key" : session['ID']+friendEmail})
        if value == 1 : # 성공
            return dbresponse.statusResponse(responseStatus=200)
        elif value == 2 : # 이미 존재하는 relation
            return dbresponse.statusResponse(responseStatus=400)
        else : # 없는 email
            return dbresponse.statusResponse(responseStatus=404)

@blueprint.route('/cancel/friend', methods=["POST"])
def cancelFriend():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        friendEmail = json['data[email]']

        if not arango.hasVertex(vertexCollection='Users', vertexId=friendEmail) : # 없는 이메일 일 경우
            return dbresponse.statusResponse(responseStatus=404)

        value = arango.removeRelation(edgeCollection='Friends', edgeKey=session['ID']+friendEmail)
        if value == 1: # 성공
            return dbresponse.statusResponse(responseStatus=200)
        elif value ==2 : # 존재하지않는 친구 연결(cancel할게 없음)
            return dbresponse.statusResponse(responseStatus=402)
        else : # 이유모르는 실패
            return dbresponse.statusResponse(responseStatus=400)


@blueprint.route('/accept/friend', methods=["POST"])
def acceptFriend():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        friendEmail = json['data[email]']

        relation = arango.isFriend(myKey=session['ID'], friendKey=friendEmail)
        if relation == 0:  # 이미 둘은 친구사이
            return dbresponse.statusResponse(responseStatus=403)
        elif relation == 2 :
            value = arango.addRelation(edgeCollection='Friends', _fromCollection='Users', _fromVertex=session['ID'],
                               _toCollection='Users', _toVertex=friendEmail,
                               content={"_key": session['ID'] + friendEmail})
            if value == 1 :# 친구 요청 수락 성공
                return dbresponse.statusResponse(responseStatus=200)
            else :
                return dbresponse.statusResponse(responseStatus=400)
        else : # 친구 요청이 없었을 경우
            return dbresponse.statusResponse(responseStatus=402)

@blueprint.route('/decline/friend', methods=["POST"])
def declineFriend():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        friendEmail = json['data[email]']

        relation = arango.isFriend(myKey=session['ID'], friendKey=friendEmail)
        if relation == 0 : # 이미 둘은 친구사이
            return dbresponse.statusResponse(responseStatus=403)
        elif relation == 2 :
            value = arango.removeRelation(edgeCollection='Friends', edgeKey=friendEmail+session['ID'])
            if value == 1 : # 성공적인 친구 요청 거절
                return dbresponse.statusResponse(responseStatus=200)
            else :
                return dbresponse.statusResponse(responseStatus=400)
        else : # 존재하지 않는 친구 요청
            return dbresponse.statusResponse(responseStatus=402)

@blueprint.route('/delete/friend', methods=["POST"])
def deleteFriend():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        friendEmail = json['data[email]']

        value = arango.isFriend(myKey=session['ID'], friendKey=friendEmail)
        if value == 0 :
            arango.removeRelation(edgeCollection='Friends', edgeKey=session['ID'] + friendEmail )
            arango.removeRelation(edgeCollection='Friends', edgeKey=friendEmail + session['ID'])
            return dbresponse.statusResponse(responseStatus=200)
        else : # 둘이서로 친구 관계가 아니거나 없는 email
            return dbresponse.statusResponse(responseStatus=400)

@blueprint.route('/search/user', methods=["POST"])
def searchUser():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        json = request.form
        searchEmail = json['data[email]']

        list = arango.searchUser(searchEmail)
        return dbresponse.searchUserResponse(userList=list, responseStatus=200)

@blueprint.route('/list/friend', methods=["POST"])
def listFriend():
    if not 'ID' in session :
        return dbresponse.statusResponse(responseStatus=401)
    else :
        list = arango.listFriend(session['ID'])
        return dbresponse.listFriendResponse(friendList=list, responseStatus=200)







@blueprint.route('/addRelation', methods=['post'])
def addRelation():
    _fromVertex = {"name":"from", "_key" : "from"}
    _toVertex = {"name": "to", "_key": "to"}
    arango.addRelation('Members', 'Users', 'from', 'Groups', 'to', {"hello":"man"})
    return "addRelation"

@blueprint.route('/removeRelation', methods=['post'])
def removeRelation():
    arango.removeRelation('Members','197796')
    return "removeRelation"

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