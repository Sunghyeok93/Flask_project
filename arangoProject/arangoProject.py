from flask import Flask, render_template, request
import arango
from arango import redis
from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "http://121.129.2.195:8080"}})
app.register_blueprint(arango.blueprint, url_prefix='/db')
app.session_interface = redis.RedisSessionInterface()
app.config.update(
    SESSION_COOKIE_NAME='ichthysgenomics_caleb_session'
)

#위 아래 origin 똑같이 맞출것
@app.after_request
def handle(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = 'http://121.129.2.195:8080'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)

