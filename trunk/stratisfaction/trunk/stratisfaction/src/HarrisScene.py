#!/usr/bin/python

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class HarrisScene(QGraphicsScene):
    def __init__(self, parser):
        QGraphicsScene.__init__(self)
        self.hp = parser
        self.svg_tree = {}
        self.selected = {}
        
    def mousePressEvent(self, event):
        currentPos = QPointF(event.scenePos())
        node = self.pointIn([currentPos.x(),currentPos.y() - self.height()])
        print node
        if node != "none":
            self.toggleSelectNode(node)
        if self.hp.mode == "edit":            
            print "jetzt auswaehlen, jetzt, jetzt!"
        else:
            if node != "none":
                #print self.selected
                if node in self.selected:        		
                    ids = set()
                    for tupel in self.hp.connections:
                        #print "tupel0: " + str(tupel[0]) + " == node: " + str(node) + " -- " + str(str(tupel[0]) == str(node))
                        if str(tupel[0]) == str(node):
                            ids.add(tupel[1])
                    #print ids
                    if self.hp.iface.activeLayer() != None:
                        for id in ids:
                            self.hp.iface.activeLayer().select(id)
                else:
                    ids = set()
                    for node in self.selected:
                        for tupel in self.hp.connections:
                            if tupel[0] == node:
                                ids.add(tupel[1])
                    if self.hp.iface.activeLayer() != None:
                        self.hp.iface.activeLayer().removeSelection()
                        for id in ids:
                            self.hp.iface.activeLayer().select(id)  
            else:
                pass 
        			    	
    def toggleSelectNode(self, node):
        if node != "none":
            if node not in self.selected:
                min_x = min(float(self.svg_tree[node][0][0]), float(self.svg_tree[node][1][0]), float(self.svg_tree[node][2][0]))
                max_x = max(float(self.svg_tree[node][0][0]), float(self.svg_tree[node][1][0]), float(self.svg_tree[node][2][0]))
                min_y = min(float(self.svg_tree[node][0][1]), float(self.svg_tree[node][1][1]), float(self.svg_tree[node][2][1]))
                max_y = max(float(self.svg_tree[node][0][1]), float(self.svg_tree[node][1][1]), float(self.svg_tree[node][2][1]))
                width = max_x - min_x
                height = max_y - min_y
                item = QGraphicsRectItem(min_x + 4, min_y + self.height() - 5, width, height)
                item.setBrush(QBrush(QColor(255,255,0,64)))
                self.addItem(item)
                self.selected[node] = item
            else:
                self.removeItem(self.selected[node])
                del self.selected[node]            
    
    def removeSelection(self):
        for node in self.selected:
            self.removeItem(self.selected[node])
        self.selected = {}
    
    def setSvg_tree(self, tree):
        self.svg_tree = tree    
        
    def pointIn(self, point):
        flag = "none"
        #print "point = " + str(point)
        if len(self.svg_tree) > 0:
            for key in self.svg_tree:
                p1 = self.svg_tree[key][0]
                p2 = self.svg_tree[key][1]
                p3 = self.svg_tree[key][2]
                p4 = self.svg_tree[key][3]
                #print "p1 = " + str(p1)
                #print "p2 = " + str(p2)
                #print "p3 = " + str(p3)
                #print "p4 = " + str(p4)
                if min(int(p1[0]), int(p2[0]), int(p3[0]), int(p4[0])) <= int(point[0]) and int(point[0]) <= max(int(p1[0]), int(p2[0]), int(p3[0]), int(p4[0])):
                    if min(int(p1[1]), int(p2[1]), int(p3[1]), int(p4[1])) <= int(point[1]) and int(point[1]) <= max(int(p1[1]), int(p2[1]), int(p3[1]), int(p4[1])):
                        flag = key
        return flag
