from Node import *
from Graph import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
from qgis.core import *
 
# initialize Qt resources from file resouces.py
import resources

class HarrisParser:

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
        print "grassify-import: run called!"

    def renderTest(self, painter):
        # use painter for drawing to map canvas
        print "grassify-import: renderTest called!"
    
    def parse(self):
        path = raw_input("Bitte Pfad zur csv-Datein angeben: ")
        fobj = open(path, "r")
        for line in fobj:
            line = line.strip()
            stratum = line.split(";")
            later = set(stratum[5].split(", "))
            earlier = set(stratum[6].split(", "))
            equal = set(stratum[7].split(", "))
            partof = set(stratum[8].split(", "))
            nodes[stratum[0]] = Node(stratum[0], stratum[1], stratum[2], stratum[3], stratum[4], later, earlier, equal, partof)
            fobj.close()
        graph = Graph(nodes)
        graph.printGraph() 
