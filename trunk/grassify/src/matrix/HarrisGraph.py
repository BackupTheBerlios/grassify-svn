from pygraphviz import *

class HarrisGraph(AGraph):
    
    def __init__(self):
        AGraph.__init__(self)
        self.__unitclass = {}
        self.__unittype = {}
        self.__description = {}
        self.__phase = {}
        self.__location = {}
    
    def add_node(self, unitname, unitclass=None, unittype=None, description=None, phase=None, location=None):
        AGraph.add_node(self, unitname)
        self.__unitclass[unitname] = unitclass or ""
        self.__unittype[unitname] = unittype or ""
        self.__description[unitname] = description or ""
        self.__phase[unitname] = phase or ""
        self.__location[unitname] = location or [0.0, 0.0]
        
          
#    def __init__(self, nodes=None):
#        self.nodes = nodes or {}
#        
#    def addNode(self, node):
#        self.nodes[node.unitname] = node
#        
#    def getNode(self, name):
#        return self.nodes[name]
#    
#    def rmNode(self, name):
#        del self.nodes[name]
#
#    def printGraph(self):
#        nodescopy = self.nodes.copy()
#        while len(nodescopy) > 0:
#            root = nodescopy.popitem()
#            print root.unitname
#            for element in root.concurrent:
#                pass
