from flask import Flask
from pyArango.connection import *

app = Flask(__name__)

def pyArangoDriver():
    conn = Connection()

    conn.createDatabase(name="test_db")
    db = self.conn[
        "test_db"]  # all databases are loaded automatically into the connection and are accessible in this fashion
    collection = db.createCollection(name="users")  # all collections are also loaded automatically

    # collection.delete() # self explanatory

    for i in range(100):
        doc = collection.createDocument()
        doc["name"] = "Tesla-%d" % i
        doc["number"] = i
        doc["species"] = "human"
        doc.save()

    doc = collection.createDocument()
    doc["name"] = "Tesla-101"
    doc["number"] = 101
    doc["species"] = "human"

    doc["name"] = "Simba"
    # doc.save() # overwrites the document
    doc.patch()  # updates the modified field
    doc.delete()


@app.route('/')
def hello_world():
    pyArangoDriver()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
