#!/usr/bin/python

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class HarrisScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        
    def mousePressEvent(self, event):
        currentPos = QPointF(event.scenePos())
        print str(currentPos.x()) + ", " + str(currentPos.y())
