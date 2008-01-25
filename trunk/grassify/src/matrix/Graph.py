class Graph:
    
    #from Node import *
    
    def __init__(self, nodes=None):
        self.nodes = nodes or {}
        
    def addNode(self, node):
        self.nodes[node.unitname] = node
        
    def getNode(self, name):
        return self.nodes[name]
    
    def rmNode(self, name):
        del self.nodes[name]

    def printGraph(self):
        nodescopy = self.nodes.copy()
        while len(nodescopy) > 0:
            root = nodescopy.popitem()
            print root.unitname
            for element in root.concurrent:
                pass
