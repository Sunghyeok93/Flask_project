from pyArango.connection import *

class arangoConnect():

    # 데이터베이스 연결 초기화
    # 데이터베이스 생성,
    def __init__(self):
        self.conn = Connection(username="root", password="")

        # main 데이터베이스 생성
        if not self.conn.hasDatabase('main_db') :
            self.db = self.conn.createDatabase('main_db')
        else :
            self.db = self.conn["main_db"]

        # 컬렉션 생성 및 확인
        if not self.db.hasCollection('users') :
            userCollection = self.db.createCollection(name="users")

        if not self.db.hasCollection('groups') :
            groupCollection = self.db.createCollection(name="groups")

