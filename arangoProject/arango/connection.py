from pyArango.connection import *
from .model import projects, mainGraph, members, users
from pyArango.theExceptions import *
import string

vertexCollections = ['Users', 'Projects','Data', 'DataBlocks', 'Pipelines']
edgeCollections = ['Members', 'Friends']
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
        for col in vertexCollections :
            if not self.db.hasCollection(col) :
                self.db.createCollection('Collection', col, name=col)

        # Edge 컬렉션 생성 및 확인
        for col in edgeCollections :
            if not self.db.hasCollection(col) :
                self.db.createCollection('Collection', col, name=col)

        # 메인 Graph 생성 및 확인
        if not self.db.hasGraph(GRAPH) :
            self.mainGraph = self.db.createGraph(name=GRAPH)

    # 그래프 내 Vertex Document 생성 / 현재 데이터베이스 설계 계획은 하나의 그래프에 모든 정보를 입력하는 것.
    # vertexCollection : 생성하고자 하는 Vertex가 속하는 Collection
    # content          : 생성한 Vertex가 가지게 될 Attribute. (전략상 _key 값 필수 입력할 것)
    # 성공적으로 Vertex를 추가 하였을 경우 True 리턴, 중복 key 값일 경우 false 리턴
    def addVertex(self, VertexCollection, content):
        try :
            vertex = self.db.graphs[GRAPH].createVertex(VertexCollection, content)
            vertex.save()
        except Exception :
            print('CONNECTION_ADDVERTEX_EXCEPTION')
            return False
        return True

    # 그래프 내 Edge Document(Relation) 생성
    # EdgeCollection  : 생성하고자 하는 Relation이 속하는 Collection
    # _fromCollection : Relation이 시작되는 Vertex가 속한 Collection
    # _fromVertex     : Relation이 시작되는 Vertex의 _key Attribute
    # _toCollection   : Relation이 끝나는 Vertex가 속한 Collection
    # _toVertex       : Relation이 끝나는 Vertex의 _key Attribute
    # content         : 생성한 Relation이 가지게 될 Attribute. (전략상 _key 값 필수 입력할 것)
    # Relation(Edge) 연결을 하고 싶은 두개의 Vertex의 _key Attribute를 알아야 한다는 조건이 존재함.
    # 성공적으로 Relation(Edge)를 추가 하였을 경우 해당 1, 실패시 0 리턴, 이미 존재하는 relation일 경우 2리턴
    def addRelation(self, edgeCollection, _fromCollection ,_fromVertex, _toCollection ,_toVertex, content):
        #try :
        if self.hasRelation(edgeCollection, _fromVertex, _toVertex) :
            return 2
        else :
            _from = self.db[_fromCollection][_fromVertex]
            _to = self.db[_toCollection][_toVertex]
            relation = self.db.graphs[GRAPH].link(edgeCollection, _from, _to, content)
            relation.save()
        #except Exception :
        #    print('CONNECTION_ADDRELATION_ERROR')
        #    return 0
        return 1

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
    # edge를 성공적으로 삭제 했을 경우 1, 실패했을경우 0 리턴, 없는 relation인 경우 2리턴
    def removeRelation(self, edgeCollection, edgeKey):
        try :
            if self.hasVertex(edgeCollection, edgeKey) :
                self.db.graphs[GRAPH].deleteEdge(self.db[edgeCollection][edgeKey])
            else :
                return 2 # 없는 relation
        except Exception :
            print('CONNECTION_REMOVERELATION_ERROR')
            return 0
        return 1 # 성공적인 삭제

    #미완성
    def returnVertex(self, VertexCollection, VertexKey):
        try :
            #aql = 'RETURN DOCUMENT("' + VertexCollection + '/'+ VertexKey+'")'
            aql = 'FOR doc IN Users RETURN doc'
            print("aql : " + aql)
            result = self.db.AQLQuery(query=aql, rawResults=True, batchSize=100)

        except Exception :
            print('CONNECTION_RETURNVERTEX_ERROR')
            return False
        return result


    #해당 컬렉션의 도큐먼트가 가지고 있는
    def getEdges(self, VertexCollection, mode, Vertex):
        col = self.db['Friends']
        print('col : ' + str(col))
        #if mode == 'in' :
        #    result = col.getInEdges('Yuha')
        #elif mode == 'out' :
        #    result = self.db.collections[VertexCollection].getOutEdges(vertex=Vertex)

        result = col.getEdges('Users/Yuha')

        for r in result :
            print(r)

        return False

    # 해당 컬렉션의 도큐먼트의 attribute가 checkValue와 같을 경우 True 리턴, 아닐경우 False 리턴
    def checkAttribute(self, collection, document, attribute, checkValue):
        if self.db[collection][document][attribute] == checkValue:
            return True
        else :
            return False

    # 해당 컬렉션의 도큐먼트 리턴
    def returnDocument(self, collection, document):
        return self.db[collection][document]

    #미완성
    def patchDocument(self, collection, document):
        json = {
            'name' : 'sunghyeok',
        }
        self.db[collection][document].reset(self.db.collections[collection], json)
        self.db[collection][document].save()
        print(self.db[collection][document])

    def hasVertex(self, vertexCollection, vertexId):
        try:
            vertex = self.db[vertexCollection][vertexId]
        except :
            return False
        return True

    # 해당 Relation이 존재할경우 True 리턴, 없을 경우 False 리턴
    def hasRelation(self, relationCollection, _fromVertex, _toVertex):
        try:
            edge = self.db[relationCollection][_fromVertex+_toVertex]
        except :
            return False
        return True
    # try :
    #   edge = myEdgesCollection.fetchFirstExample({"_to": doc2._id, "_from": doc1._id})[0]
    # except :
    #   edge = myGraph("myEdgesCollection", doc1, doc2, {})


    # 둘이 친구 관계 일경우 0 리턴
    # 나만 친구 요청을 보냈을 경우 1, 상대만 내게 친구 요청을 보냈을 경우 2 리턴, 아무것도 없으면 3 리턴
    def isFriend(self, myKey, friendKey):
        if self.hasRelation('Friends', myKey, friendKey) & self.hasRelation('Friends', friendKey, myKey):
            return 0
        elif self.hasRelation('Friends', myKey, friendKey) :
            return 1
        elif self.hasRelation('Friends', friendKey, myKey) :
            return 2
        else :
            return 3

    #email을 이용한 검색 유저 반환
    def searchUser(self, email):
        aql = 'FOR doc in Users FILTER doc._key LIKE "' + email + '%" return doc'
        queryResult = self.db.AQLQuery(aql, rawResults=False, batchSize=10)
        return queryResult

    #
    def listFriend(self, _key):
        inEdge = []
        outEdge = []
        allEdge = []
        col = self.db['Friends']
        result1 = col.getInEdges('Users/'+_key)
        result2 = col.getOutEdges('Users/' + _key)

        for doc in result1 :
            val = {'email':doc['_from'][6:], 'name':doc['name']}
            inEdge.append(val)
        for doc in result2:
            val = {'email': doc['_to'][6:], 'name': doc['name']}
            outEdge.append(val)
        for edge in inEdge :
            if outEdge.count(edge) == 1 :
                allEdge.append(edge)
                inEdge.remove(edge)
                outEdge.remove(edge)

        for doc in inEdge :
            doc['relation'] = 2
        for doc in outEdge:
            doc['relation'] = 1
        for doc in allEdge:
            doc['relation'] = 0

        return inEdge + outEdge + allEdge
    # _key 입력시 해당 도큐먼트 내용 주는 기능



