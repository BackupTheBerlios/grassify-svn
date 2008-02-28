#from Node import *
from HarrisGraph import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
from qgis.core import *
 
# initialize Qt resources from file resouces.py
import resources

class GrassifyPlugin:

    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        self.nodes = {}

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/grassify/icon.xpm"), "grassify plugin", self.iface.getMainWindow())
        self.action.setWhatsThis("Configuration for grassify plugin")
        QObject.connect(self.action, SIGNAL("activated()"), self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginMenu("&grassify plugins", self.action)

        # connect to signal renderComplete which is emitted when canvas rendering is done
        QObject.connect(self.iface.getMapCanvas(), SIGNAL("renderComplete(QPainter *)"), self.renderTest)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&grassify plugins",self.action)
        self.iface.removeToolBarIcon(self.action)

        # disconnect form signal of the canvas
        QObject.disconnect(self.iface.getMapCanvas(), SIGNAL("renderComplete(QPainter *)"), self.renderTest)


    def run(self):
        # create and show a configuration dialog or something similar
        # print "grassify-import: run called!"
        self.parse("testmatrix.csv")

    def renderTest(self, painter):
        # use painter for drawing to map canvas
        print "grassify-import: renderTest called!"
    
    def parse(self, path):
        fobj = open(path, "r")
        graph = HarrisGraph()
        graph.node_attr['shape'] = 'box'
        # Knoten hinzufuegen
        for line in fobj:
            line = line.strip()
            stratum = line.split(";")
            if stratum[1] == "context":
                graph.add_node(stratum[0], stratum[1], stratum[2], stratum[3], stratum[4])
        # Kanten hinzufuegen
        fobj.close()
        fobj = open(path, "r")
        for line in fobj:
            line = line.strip()
            stratum = line.split(";")
            unitname = stratum[0]
            later = set(stratum[5].split(", "))
            if stratum[1] == "context":
                for node in later:
                    if node != "":
                        graph.add_edge(unitname, node, "later")
                earlier = set(stratum[6].split(", "))
                for node in earlier:
                    if node != "":
                        graph.add_edge(node, unitname, "earlier")
                equal = set(stratum[7].split(", "))
#                for node in equal:
#                    if node != "":
#                        graph.add_edge(unitname, node, "concurrent")
#                partof = set(stratum[8].split(", "))
#                for node in partof:
#                    if node != "":
#                        graph.add_edge(unitname, node, "concurrent")            
        fobj.close()
        neighbors = graph.neighbors("103")
        for n in neighbors:
            print(n)
        print graph.string() # print to screen
        graph.write("matrix.dot") # write to simple.dot
        print "Wrote matrix.dot"
        graph.layout(prog='dot')
        graph.draw('matrix.svg') # draw to png 
        print "Wrote matrix.png"