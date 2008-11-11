from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ImageViewer(QMainWindow):
    
    def __init__(self):
        self.__imageLabel = QLabel()
        self.__imageLabel.setBackgroundRole(QPalette.Base)
        self.__imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.__imageLabel.setScaledContents(True);
        
        self.__scrollArea = QScrollArea()
        self.__scrollArea.setBackgroundRole(QPalette.Dark)
        self.__scrollArea.setWidget(self.__imageLabel)
        
        self.__scaleFactor
        self.__printer = QPrinter()
        self.__openAct = QAction()
        self.__printAct = QAction()
        self.__exitAct = QAction()
        self.__zoomInAct = QAction()
        self.__zoomOutAct = QAction()
        self.__normalSizeAct = QAction()
        self.__fitToWindowAct = QAction()
        self.__aboutAct = QAction()
        self.__aboutQtAct = QAction()
        self.__fileMenu = QMenu()
        self.__viewMenu = QMenu()
        self.__helpMenu = QMenu()
        
        self.setCentralWidget(self.__scrollArea)
        
        self.__createActions();
        self.__createMenus();
        
        self.setWindowTitle(self.tr("Image Viewer"))
        self.resize(500, 400)
    
    def __open(self):
        fileName = QFileDialog.getOpenFileName(self, self.tr("Open File"), ".")
        if not fileName.isEmpty():
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, tr("Image Viewer"), tr("Cannot load " + fileName))
                return
            self.__imageLabel.setPixmap(QPixmap.fromImage(image))
            self.__scaleFactor = 1.0
            
            self.__printAct.setEnabled(True)
            self.__fitToWindowAct.setEnabled(True)
            self.__updateActions()
            
            if not self.__fitToWindowAct.isChecked():
                self.__imageLabel.adjustSize()
    
    def __print(self):
        #self.Q_ASSERT(self.__imageLabel.pixmap())
        dialog = QPrintDialog(self.__printer, self)
        if dialog.exec_():
            painter = QPainter(self.__printer)
            rect = QRect(painter.viewport())
            size = QSize(self.__imageLabel.pixmap().size())
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.__imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.__imageLabel.pixmap())
    
    def __zoomIn(self):
        self.__scaleImage(1.25)
    
    def __zoomOut(self):
        self.__scaleImage(0.8)
        
    def __normalSize(self):
        self.__imageLabel.adjustSize()
        self.__scaleFactor = 1.0
        
    def __fitToWindow(self):
        fitToWindow = self.__fitToWindowAct.isChecked()
        self.__scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.__normalSize()
            self.__updateActions()
    
    def __about(self):
        QMessageBox.about(self, tr("About Image Viewer"), 
             tr("<p>The <b>Image Viewer</b> example shows how to combine QLabel "
                "and QScrollArea to display an image. QLabel is typically used "
                "for displaying a text, but it can also display an image. "
                "QScrollArea provides a scrolling view around another widget. "
                "If the child widget exceeds the size of the frame, QScrollArea "
                "automatically provides scroll bars. </p><p>The example "
                "demonstrates how QLabel's ability to scale its contents "
                "(QLabel::scaledContents), and QScrollArea's ability to "
                "automatically resize its contents "
                "(QScrollArea::widgetResizable), can be used to implement "
                "zooming and scaling features. </p><p>In addition the example "
                "shows how to use QPainter to print an image.</p>"))
    
    def __createActions(self):
        openAct = QAction(tr("&Open..."), self)
        openAct.setShortcut(tr("Ctrl+O"))
        self.connect(openAct, SIGNAL(QAction.activated()), self, SLOT(open()))
 
 
 
# void ImageViewer::createActions()
# {
#     openAct = new QAction(tr("&Open..."), this);
#     openAct->setShortcut(tr("Ctrl+O"));
#     connect(openAct, SIGNAL(triggered()), this, SLOT(open()));
#
#     printAct = new QAction(tr("&Print..."), this);
#     printAct->setShortcut(tr("Ctrl+P"));
#     printAct->setEnabled(false);
#     connect(printAct, SIGNAL(triggered()), this, SLOT(print()));
#
#     exitAct = new QAction(tr("E&xit"), this);
#     exitAct->setShortcut(tr("Ctrl+Q"));
#     connect(exitAct, SIGNAL(triggered()), this, SLOT(close()));
#
#     zoomInAct = new QAction(tr("Zoom &In (25%)"), this);
#     zoomInAct->setShortcut(tr("Ctrl++"));
#     zoomInAct->setEnabled(false);
#     connect(zoomInAct, SIGNAL(triggered()), this, SLOT(zoomIn()));
#
#     zoomOutAct = new QAction(tr("Zoom &Out (25%)"), this);
#     zoomOutAct->setShortcut(tr("Ctrl+-"));
#     zoomOutAct->setEnabled(false);
#     connect(zoomOutAct, SIGNAL(triggered()), this, SLOT(zoomOut()));
#
#     normalSizeAct = new QAction(tr("&Normal Size"), this);
#     normalSizeAct->setShortcut(tr("Ctrl+S"));
#     normalSizeAct->setEnabled(false);
#     connect(normalSizeAct, SIGNAL(triggered()), this, SLOT(normalSize()));
#
#     fitToWindowAct = new QAction(tr("&Fit to Window"), this);
#     fitToWindowAct->setEnabled(false);
#     fitToWindowAct->setCheckable(true);
#     fitToWindowAct->setShortcut(tr("Ctrl+F"));
#     connect(fitToWindowAct, SIGNAL(triggered()), this, SLOT(fitToWindow()));
#
#     aboutAct = new QAction(tr("&About"), this);
#     connect(aboutAct, SIGNAL(triggered()), this, SLOT(about()));
#
#     aboutQtAct = new QAction(tr("About &Qt"), this);
#     connect(aboutQtAct, SIGNAL(triggered()), qApp, SLOT(aboutQt()));
# }
#
# void ImageViewer::createMenus()
# {
#     fileMenu = new QMenu(tr("&File"), this);
#     fileMenu->addAction(openAct);
#     fileMenu->addAction(printAct);
#     fileMenu->addSeparator();
#     fileMenu->addAction(exitAct);
#
#     viewMenu = new QMenu(tr("&View"), this);
#     viewMenu->addAction(zoomInAct);
#     viewMenu->addAction(zoomOutAct);
#     viewMenu->addAction(normalSizeAct);
#     viewMenu->addSeparator();
#     viewMenu->addAction(fitToWindowAct);
#
#     helpMenu = new QMenu(tr("&Help"), this);
#     helpMenu->addAction(aboutAct);
#     helpMenu->addAction(aboutQtAct);
#
#     menuBar()->addMenu(fileMenu);
#     menuBar()->addMenu(viewMenu);
#     menuBar()->addMenu(helpMenu);
# }
#
# void ImageViewer::updateActions()
# {
#     zoomInAct->setEnabled(!fitToWindowAct->isChecked());
#     zoomOutAct->setEnabled(!fitToWindowAct->isChecked());
#     normalSizeAct->setEnabled(!fitToWindowAct->isChecked());
# }
#
# void ImageViewer::scaleImage(double factor)
# {
#     Q_ASSERT(imageLabel->pixmap());
#     scaleFactor *= factor;
#     imageLabel->resize(scaleFactor * imageLabel->pixmap()->size());
#
#     adjustScrollBar(scrollArea->horizontalScrollBar(), factor);
#     adjustScrollBar(scrollArea->verticalScrollBar(), factor);
#
#     zoomInAct->setEnabled(scaleFactor < 3.0);
#     zoomOutAct->setEnabled(scaleFactor > 0.333);
# }
#
# void ImageViewer::adjustScrollBar(QScrollBar *scrollBar, double factor)
# {
#     scrollBar->setValue(int(factor * scrollBar->value()
#                             + ((factor - 1) * scrollBar->pageStep()/2)));
# }
#            
#            
#        
#            
#            
#            
#        