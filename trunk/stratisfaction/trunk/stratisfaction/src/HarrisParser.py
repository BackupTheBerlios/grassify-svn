#!/usr/bin/python

# harrisparser.py

import sys
import svgparser
from HarrisGraph import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from qgis.core import *
from qgis.gui import *


class HarrisParser(QMainWindow):
    def __init__(self, iface, parent=None):
        QMainWindow.__init__(self, parent)

        self.iface = iface
        
        self.setGeometry(300, 300, 355, 352)
        self.setWindowTitle('Stratisfaction')

        self.textEdit = QTextEdit()
        
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setGeometry(300, 300, 350, 300)
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        
        #grid = QtGui.QGridLayout()
        #grid.setSpacing(10)
        #grid.addWidget(self.scrollArea, 1, 0)
        #grid.addWidget(self.textEdit, 2, 0)
        
        #self.setLayout(grid)
        
        self.setCentralWidget(self.scrollArea)
        #self.setCentralWidget(self.textEdit)
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
        
        #self.makeConnections()
        
    #def makeConnections(self):
        #self.layer = self.iface.activeLayer()
        #print type(self.layer)
        #print(self.connect(self.iface, SIGNAL("currentLayerChanged (QgsMapLayer *layer)"), self.showSelected))    
        
    def showDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.parse(filename)
        self.draw("matrix.svg")
        svg_tree = svgparser.lade_svg("matrix.svg")
        
    def mousePressEvent(self, event):
        if event.button()== Qt.LeftButton:
            return QPoint(event.pos())
            #print "Schalke ist der geilste Klup der Welt"
        
    
        
        
        ########################################################################
        # 
        #  svg_tree enthaelt die koordinaten der rechtecke.
        #  svg_tree[id][koordinate][x|y]
        #  also svg_tree[1][3][y] liefert euch die y-koordinate des 3. Punktes
        #  von polygon 1 
        #
        #  jetzt also per mouseclickevent die aktuelle koordinate auslesen und
        #  ueberpruefen ob die in einem der rechtecke liegt. haut rein!
        #
        ########################################################################
        svgparser.printMoped(svg_tree)
        #file=open(filename)
        #data = file.read()
        #self.textEdit.setText(data)
        
    def mouseMoveEvent(self, event):
        currentPos = QPoint(event.pos())
        self.statusBar().showMessage(str(currentPos.x() - 6) + ", " + str(currentPos.y() - 790))

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
                graph.add_node(stratum[0], stratum[1], stratum[2], stratum[3], stratum[4])
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
            later = set(stratum[5].split(", "))
            if stratum[1] == "context":
                for node in later:
                    if node != "":
                        graph.add_edge(unitname, node, "later")
                earlier = set(stratum[6].split(", "))
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
        print graph.string() # print to screen
        graph.write("matrix.dot") # write to simple.dot
        print "Wrote matrix.dot"
        graph.layout(prog='dot')
        graph.draw('matrix.svg') # draw to png 
        print "Wrote matrix.png"
        
    def draw(self, path):
        image = QImage(path)
        pixmap = QPixmap.fromImage(image)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(self.imageLabel.pixmap().size())    
        self.resize(self.imageLabel.pixmap().size())  

#app = QtGui.QApplication(sys.argv)
#hp = HarrisParser()
#hp.show()
#app.exec_()
