from pyArango.graph import Graph, EdgeDefinition

class mainGraph(Graph) :
    _edgeDefinitions = [EdgeDefinition("Members", fromCollections=["Users"], toCollections=["Projects"]),
                        EdgeDefinition("Friends",fromCollections=["Users"], toCollections=['Users'])]
    _orphanedCollections = []
