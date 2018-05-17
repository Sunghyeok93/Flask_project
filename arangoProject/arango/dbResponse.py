from flask import json, Response
from collections import OrderedDict


# 접속 세션인 없는 경우 status 401
# 성공적으로 기능 수행시 status 200
class arangoResponse():

    def statusResponse(self, responseStatus):
        data = {
            'status' : responseStatus
        }
        js = json.dumps(data)
        resp = Response(js, status=responseStatus, mimetype='application/json')
        return resp

    def userResponse(self, email, name, pwd, desc, responseStatus):
        data = {
            'email' : email,
            'name' : name,
            'pwd' : pwd,
            'desc' : desc,
            'status': responseStatus
        }
        js = json.dumps(data)
        resp = Response(js, status=responseStatus, mimetype='application/json')
        return resp

    def searchUserResponse(self, userList, responseStatus):
        list = []
        data = {
            'status' : responseStatus
        }

        for user in userList :
            val = {'email':user['_key'], 'name':user['name']}
            list.append(val)
        data['list'] = list

        js = json.dumps(data)

        return Response(js,status=responseStatus, mimetype='application/json')

    def listFriendResponse(self,friendList, responseStatus):
        data = {
            'status': responseStatus,
            'list' : friendList
        }
        js = json.dumps(data)
        resp = Response(js, status=responseStatus, mimetype='application/json')
        return resp