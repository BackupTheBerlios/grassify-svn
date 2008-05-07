#!/usr/bin/python

# harrisparser.py

import sys
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
        
        scrollArea = QScrollArea()
        scrollArea.setBackgroundRole(QPalette.Dark)
        scrollArea.setWidget(self.imageLabel)
        
        #grid = QtGui.QGridLayout()
        #grid.setSpacing(10)
        #grid.addWidget(scrollArea, 1, 0)
        #grid.addWidget(self.textEdit, 2, 0)
        
        #self.setLayout(grid)
        
        self.setCentralWidget(scrollArea)
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
        
        self.layer = self.iface.activeLayer()
        if self.layer.type() == 0:
            self.connect(self.layer, SIGNAL("selectionChanged()"), self.showSelected)
            
        
    def showDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.parse(filename)
        #file=open(filename)
        #data = file.read()
        #self.textEdit.setText(data)
        
#    def mouseMoveEvent(self, event):
#        currentPos = QtCore.QPoint(event.pos())
#        self.statusBar().showMessage(str(currentPos.x()) + ", " + str(currentPos.y()))

    def showSelected(self):
        layer = self.iface.activeLayer()
        featureIDs = layer.selectedFeaturesIds()
        for id in featureIDs:
            print id 
    
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
        self.draw("matrix.svg")
        
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