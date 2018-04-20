from pyArango.connection import *
from .model import projects, mainGraph, members, users
from pyArango.theExceptions import *

vertexCollections = ['Users', 'Groups']
edgeCollections = ['Members', 'Projects']
GRAPH = 'mainGraph'
DATABASE = 'main_db'

class arangoConnect():

    # 데이터베이스 연결 초기화
    def __init__(self):
        self.conn = Connection(username="root", password="")

        # main 데이터베이스 생성
        if not self.conn.hasDatabase(DATABASE) :
            self.db = self.conn.createDatabase(DATABASE)
        else :
            self.db = self.conn[DATABASE]

        # Vertex 컬렉션 생성 및 확인
        if not self.db.hasCollection('Users') :
            self.userCollection = self.db.createCollection('Collection', "Users", name="Users")

        if not self.db.hasCollection('Projects') :
            self.groupCollection = self.db.createCollection('Collection', "Projects", name="Projects")

        # Edge 컬렉션 생성 및 확인
        if not self.db.hasCollection('Members') :
            self.memberCollection = self.db.createCollection('Edges', "Members", name="Members")

        if not self.db.hasCollection('Friends') :
            self.memberCollection = self.db.createCollection('Edges', "Friends", name="Friends")

        # 메인 Graph 생성 및 확인
        if not self.db.hasGraph(GRAPH) :
            self.mainGraph = self.db.createGraph(name=GRAPH)

    # 그래프 내 Vertex Document 생성 / 현재 데이터베이스 설계 계획은 하나의 그래프에 모든 정보를 입력하는 것.
    # vertexCollection : 생성하고자 하는 Vertex가 속하는 Collection
    # content          : 생성한 Vertex가 가지게 될 Attribute. (전략상 _key 값 필수 입력할 것)
    # 성공적으로 Vertex를 추가 하였을 경우 해당 vertex doc 리턴, 실패시 False 리턴
    def addVertex(self, VertexCollection, content):
        try :
            vertex = self.db.graphs[GRAPH].createVertex(VertexCollection, content)
            vertex.save()
        except pyArangoException :
            print('CONNECTION_ADDVERTEX_ERROR')
            return False
        return vertex

    # 그래프 내 Edge Document(Relation) 생성
    # EdgeCollection  : 생성하고자 하는 Relation이 속하는 Collection
    # _fromCollection : Relation이 시작되는 Vertex가 속한 Collection
    # _fromVertex     : Relation이 시작되는 Vertex의 _key Attribute
    # _toCollection   : Relation이 끝나는 Vertex가 속한 Collection
    # _toVertex       : Relation이 끝나는 Vertex의 _key Attribute
    # content         : 생성한 Relation이 가지게 될 Attribute. (전략상 _key 값 필수 입력할 것)
    # Relation(Edge) 연결을 하고 싶은 두개의 Vertex의 _key Attribute를 알아야 한다는 조건이 존재함.
    # 성공적으로 Relation(Edge)를 추가 하였을 경우 해당 relation doc 리턴, 실패시 False 리턴
    def addRelation(self, edgeCollection, _fromCollection ,_fromVertex, _toCollection ,_toVertex, content):
        #print(self.db[_fromCollection][_fromVertex])
        #print(self.db[_fromCollection][_fromVertex]['name'])
        try :
            _from = self.db[_fromCollection][_fromVertex]
            _to = self.db[_toCollection][_toVertex]
            relation = self.db.graphs[GRAPH].link(edgeCollection, _from, _to, content)
            relation.save()
        except pyArangoException :
            print('CONNECTION_ADDRELATION_ERROR')
            return False
        return relation

    # 그래프네의 Vertex 삭제
    # vertexCollection : 삭제하고자 하는 Vertex가 속한 Collection
    # vertexKey        : 삭제하고자 하는 Vertex의 _key 값
    # Vertex를 성공적으로 삭제 했을 경우 True, 실패했을경우 False 리턴
    def removeVertex(self, vertexCollection, vertexKey):
        try :
            self.db.graphs[GRAPH].deleteVertex(self.db[vertexCollection][vertexKey])
        except Exception :
            print('CONNECTION_REMOVEVERTEX_ERROR')
            return False
        return True

    # 그래프네의 Edge(Relation) 삭제
    # edgeCollection : 삭제하고자 하는 Edge가 속한 Collection
    # edgeKey        : 삭제하고자 하는 Edge의 _key 값
    # edge를 성공적으로 삭제 했을 경우 True, 실패했을경우 False 리턴
    def removeRelation(self, edgeCollection, edgeKey):
        try :
            self.db.graphs[GRAPH].deleteEdge(self.db[edgeCollection][edgeKey])
        except Exception :
            print('CONNECTION_REMOVERELATION_ERROR')
            return False
        return True
