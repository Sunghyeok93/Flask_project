from flask import Blueprint, request, render_template
from . import document

blueprint = Blueprint('_arango', __name__)

@blueprint.route('/')
def hello_world():
    return render_template('main.html')

@blueprint.route('/11', methods=["POST"])
def createVertexDocument():
    vertexName = request.form['vertexName']
    return vertexName

@blueprint.route('/createEdgeDocument', methods=['post'])
def createEdgeDocument():
    edgeName = request.form['edgeName']
    _from = request.form['_from']
    _to = request.form['_to']
    return edgeName+_from+_to
