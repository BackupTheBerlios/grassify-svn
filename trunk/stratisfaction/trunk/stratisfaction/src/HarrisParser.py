#!/usr/bin/python

# harrisparser.py

import sys
import svgparser
from HarrisGraph import *
from HarrisScene import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSvg import *

from qgis.core import *
from qgis.gui import *


class HarrisParser(QMainWindow):
    def __init__(self, iface, parent=None):
        QMainWindow.__init__(self, parent)

        self.svg_tree = {}
        self.iface = iface
        
        self.setGeometry(300, 300, 355, 352)
        self.setWindowTitle('Stratisfaction')

        
        self.scene = HarrisScene()
        self.view = QGraphicsView(self.scene)
        
        self.view.show()
        
        self.setCentralWidget(self.view)
        self.statusBar()
        self.setFocus()

        opan = QAction(QIcon('open.png'), 'Open', self)
        opan.setShortcut('Ctrl+O')
        opan.setStatusTip('Open new File')
        self.connect(opan, SIGNAL('triggered()'), self.showDialog)
        
        exit = QAction(QIcon('exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(opan)
        file.addAction(exit)
        
    def showDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.parse(filename)
        self.draw("matrix.svg")
        self.svg_tree = svgparser.lade_svg("matrix.svg")
        self.scene.setSvg_tree(self.svg_tree)
        
    def showSelected(self):
        layer = self.iface.activeLayer()
        print type(layer)
        if isinstance(layer, QgsVectorLayer):
        #if layer.type() == QgsMapLayer.VECTOR:
            featureIDs = layer.selectedFeaturesIds()
            ids = ""
            for id in featureIDs:
                ids = ids + ", " + str(id)
            self.imageLabel.setText("Gewaehlte Features: \n \n" + ids)
    
    def parse(self, path):
        fobj = open(path, "r")
        graph = HarrisGraph()
        graph.node_attr['shape'] = 'box'
        groups = dict()
        # Knoten hinzufuegen, Gruppen erzeugen
        for line in fobj:
            line = line.strip()
            stratum = line.split(";")
            if stratum[1] == "context":
                graph.add_node(stratum[0], stratum[1])
                #graph.add_node(stratum[0], stratum[1], stratum[2], stratum[3], stratum[4])
#            if stratum[1] == "group":
#                groups[stratum[0]] = set()              
        # Kanten hinzufuegen, Knoten zu Gruppen zuordnen
        fobj.close()
        fobj = open(path, "r")
        index = 0
        for line in fobj:
            line = line.strip()
            stratum = line.split(";")
            unitname = stratum[0]
            later = set(stratum[2].split(", "))
            if stratum[1] == "context":
                for node in later:
                    if node != "":
                        graph.add_edge(unitname, node, "later")
                earlier = set(stratum[3].split(", "))
                for node in earlier:
                    if node != "":
                        graph.add_edge(node, unitname, "earlier")
#                group = set(stratum[8].split(", "))
#                for g in group:
#                    if g in groups:
#                        groups[g].add(unitname)
#                equal = set(stratum[7].split(", "))
#                for node in equal:
#                    if node != "":
#                        graph.add_edge(unitname, node, "concurrent")
#                partof = set(stratum[8].split(", "))
#                for node in partof:
#                    if node != "":
#                        graph.add_edge(unitname, node, "concurrent")            
        fobj.close()
#        for key in groups:
#           graph.add_subgraph(groups[key], key)
#        neighbors = graph.neighbors("103")
#        for n in neighbors:
#            print(n)
        #print graph.string() # print to screen
        graph.write("matrix.dot") # write to simple.dot
        print "Wrote matrix.dot"
        graph.layout(prog='dot')
        graph.draw('matrix.svg') # draw to png 
        print "Wrote matrix.png"
        
    def draw(self, path): 
        item = QGraphicsSvgItem(path)
        self.scene.addItem(item)
        #print "hoehe: " + str(self.scene.height())

#app = QtGui.QApplication(sys.argv)
#hp = HarrisParser()
#hp.show()
#app.exec_()
