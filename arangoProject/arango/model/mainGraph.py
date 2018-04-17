from pyArango.graph import Graph, EdgeDefinition

class mainGraph(Graph) :
    _edgeDefinitions = [EdgeDefinition("Members", fromCollections=["Users"], toCollections=["Groups"])]
    _orphanedCollections = []
