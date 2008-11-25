#!/usr/bin/python

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class HarrisScene(QGraphicsScene):
    def __init__(self, parser):
        QGraphicsScene.__init__(self)
        self.hp = parser
        self.svg_tree = {}
        
        
    def mousePressEvent(self, event):
        currentPos = QPointF(event.scenePos())
        #print str(currentPos.x()) + ", " + str(currentPos.y() - self.height())
        node = self.pointIn([currentPos.x(),currentPos.y() - self.height()])
        print node
        if self.hp.mode == "edit":
            self.hp.selected = node
            print "jetzt auswaehlen, jetzt, jetzt!"
    
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
