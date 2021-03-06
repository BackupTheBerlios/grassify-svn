#!/usr/bin/python

# harrisparser.py

import sys
import os
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
        self.iface = iface

        self.projname = "Harris"
        self.path = os.environ['HOME']
        
        self.connections = set()
        
        self.mode = "interact"
        
        self.svg_tree = {}
        
        
        self.setGeometry(300, 300, 390, 400)
        self.setWindowTitle('Stratisfaction')

        
        self.scene = HarrisScene(self)
        self.view = QGraphicsView(self.scene)
        
        startscreen = QPixmap(':startscreen.png')
        self.scene.addItem(QGraphicsPixmapItem(startscreen))
        
        self.view.show()
        
        self.setCentralWidget(self.view)
        self.statusBar()
        self.setFocus()
        
        os.chdir(self.path)
                
        new = QAction(QIcon(':document-new.png'), 'New', self)
        new.setShortcut('Ctrl+N')
        new.setStatusTip('Create new Project')
        self.connect(new, SIGNAL('triggered()'), self.showNewDialog)

        opan = QAction(QIcon(':document-open.png'), 'Open', self)
        opan.setShortcut('Ctrl+O')
        opan.setStatusTip('Open Project File')
        self.connect(opan, SIGNAL('triggered()'), self.opan)
        
        impert = QAction(QIcon(':document-import.png'), 'Import Stratify Data', self)
        impert.setShortcut('Ctrl+I')
        impert.setStatusTip('Import Data from Stratify')
        self.connect(impert, SIGNAL('triggered()'), self.showImportDialog)
        
        save = QAction(QIcon(':document-save.png'), 'Save', self)
        save.setShortcut('Ctrl+S')
        save.setStatusTip('Save Project')
        self.connect(save, SIGNAL('triggered()'), self.save)
        
        exit = QAction(QIcon(':application-exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))
        
        switch = QAction(QIcon(':edit.png'), 'Switch mode', self)
        switch.setShortcut('Ctrl+E')
        switch.setStatusTip('Switch to Editmode')
        self.connect(switch, SIGNAL('triggered()'), self.edit)

# ein versuch die layer ids per knopfdruck anzuzeigen
#        showId = QAction(self)
#        self.connect(showId, SIGNAL('triggered()'), self.getLayerId)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(new)
        file.addAction(opan)
        file.addAction(save)
        file.addAction(impert)
        file.addAction(exit)
        
        edit = menubar.addMenu('&Edit')
        edit.addAction(switch)
        
         # Add a shortcut toolbar
        self.toolbar = self.addToolBar('Tooli')
        self.toolbar.addAction(new)
        self.toolbar.addAction(opan)
        self.toolbar.addAction(save)
        self.toolbar.addAction(impert)
        self.toolbar.addAction(exit)
        
#        self.toolbar2 = self.addToolBar('Tuwas')
#        self.toolbar2.addAction(showId)

#    def getLayerId(self):
#        eidi = iface.QgisInterface.QgsMapLayer.QgsVectorLayer.selectedFeaturesIds
#        print eidi
    
    def showImportDialog(self):
        filename = str(QFileDialog.getOpenFileName(self, 'Open file', '/home', 'CSV-Dateien (*.csv)'))
        if filename != "":
            self.parse(filename)
            self.draw(self.projname + ".svg")
            self.svg_tree = svgparser.lade_svg(self.projname + ".svg")
            self.scene.setSvg_tree(self.svg_tree)
        
    def showNewDialog(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix("spf")
        filename = str(dialog.getSaveFileName(self, 'Set Project File', '/home', 'Stratisfaction Project File (*.spf)'))
        print filename
        puzzle = filename.rsplit("/", 1)
        os.chdir(puzzle[0])
        self.projname = puzzle[1]
        print self.projname
        
    def save(self):
        if self.iface.activeLayer() != None and self.iface.activeLayer().type() == QgsMapLayer.VECTOR:        
            fobj = open(self.projname + ".spf", "w") 
            fobj.write("layer_path=" + self.iface.activeLayer().source() + "\n") 
            for connection in self.connections: 
                fobj.write("connection=" + str(connection[0]) + "-" + str(connection[1]) + "\n") 
            fobj.close()
        else:
            QMessageBox.critical(self, "No Layer", "Please load at least one Vectorlayer!", QMessageBox.Ok)

    def opan(self):
        #self.iface.newProject()
        filename = str(QFileDialog.getOpenFileName(self, 'Open project file', '/home', 'stratisfaction project files (*.spf)'))
        if filename != "":
            projpath = filename.rsplit(".", 1)
            self.draw(projpath[0] + ".svg")
            self.svg_tree = svgparser.lade_svg(projpath[0] + ".svg")
            self.scene.setSvg_tree(self.svg_tree)
            fobj = open(filename, "r")
            for line in fobj:
                eintrag = line.split("=");
                if eintrag[0] == "layer_path":
                    print str(eintrag[1])
                    #self.iface.addVectorLayer(eintrag[1], "Ausgrabung", "ogr")
                elif eintrag[0] == "connection":
                    connection = eintrag[1].split("-")
                    self.connections.add((int(connection[0]), int(connection[1])))
            print self.connections
                
                
        
        
#    def showSelected(self):
#        layer = self.iface.activeLayer()
#        print type(layer)
#        if isinstance(layer, QgsVectorLayer):
#        #if layer.type() == QgsMapLayer.VECTOR:
#            featureIDs = layer.selectedFeaturesIds()
#            ids = ""
#            for id in featureIDs:
#                ids = ids + ", " + str(id)
#            self.imageLabel.setText("Gewaehlte Features: \n \n" + ids)
    
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
        graph.write(self.projname + ".dot") # write to simple.dot
        print "Wrote matrix.dot"
        graph.layout(prog='dot')
        graph.draw(self.projname + '.svg') # draw to png 
        print "Wrote matrix.png"
        
    def draw(self, path): 
        item = QGraphicsSvgItem(path)
        self.scene.addItem(item)
        #print "hoehe: " + str(self.scene.height())
        
    def edit(self):
        if self.iface.activeLayer() != None and self.iface.activeLayer().type() == QgsMapLayer.VECTOR:  
            if len(self.scene.items()) > 0:     
                self.scene.removeSelection()
                self.iface.activeLayer().removeSelection()
                if self.mode == "interact":
                    self.mode = "edit"
                    self.button = QPushButton("zuweisen", self)
                    self.connect(self.button, SIGNAL('clicked()'), self.makeConnections)
                    self.statusBar().addWidget(self.button)
                    self.button.show()
                    print self.mode + " mode activatet"
                else:
                    self.mode = "interact"
                    self.statusBar().removeWidget(self.button)
                    print self.mode + "ion mode activatet"
            else:
                QMessageBox.critical(self, "No Matrix", "Please open an existing Project or\nimport some Stratify data before editing!", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "No Layer", "Please load at least one Vectorlayer!", QMessageBox.Ok)
            
    def makeConnections(self):
        if self.scene.selected != {}:
            if self.iface.activeLayer() != None and self.iface.activeLayer().type() == QgsMapLayer.VECTOR:
                if int(self.iface.activeLayer().selectedFeatureCount()) >= 1:            
                    for node in self.scene.selected:
                        featuresIds = self.iface.activeLayer().selectedFeaturesIds()
                        for id in featuresIds:
                            self.connections.add((int(node), int(id)))
                    print self.connections
                else:
                    QMessageBox.critical(self, "No Selection", "Please select at least one feature!", QMessageBox.Ok)     
            else:
                QMessageBox.critical(self, "No Layer", "Please load at least one Vectorlayer!", QMessageBox.Ok)           
        else:
            QMessageBox.critical(self, "No Selection", "Please select at least one node!", QMessageBox.Ok)
            
    def toggleSelected(self, node):
        if node in self.scene.selected:
            self.scene.selected.remove(node)
        else:
            self.scene.selected.add(node)

#app = QtGui.QApplication(sys.argv)
#hp = HarrisParser()
#hp.show()
#app.exec_()
