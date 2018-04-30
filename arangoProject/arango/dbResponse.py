from flask import json, Response

class arangoResponse():

    def statusResponse(self, responseStatus):
        data = {
            'status' : responseStatus
        }
        js = json.dumps(data)

        resp = Response(js, status=responseStatus, mimetype='application/json')
        return resp

