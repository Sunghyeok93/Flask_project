from flask import Flask, render_template
import arango

app = Flask(__name__)
app.register_blueprint(arango.blueprint)
#app.register_blueprint(_arango.blueprint , url_prefix='/pages')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
