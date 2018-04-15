from flask import Blueprint, request, render_template
from . import collection, connection
from arango.model import *

blueprint = Blueprint('_arango', __name__)


@blueprint.route('/')
def hello_world():
    connection.arangoConnect()
    return render_template('main.html')


@blueprint.route('/createVertexEdge', methods=["POST"])
def createVertexDocument():
    vertexName = request.form['vertexName']
    return vertexName


@blueprint.route('/createEdgeDocument', methods=['post'])
def createEdgeDocument():
    edgeName = request.form['edgeName']
    _from = request.form['_from']
    _to = request.form['_to']
    return edgeName+_from+_to
