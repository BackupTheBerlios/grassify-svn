import sys
from PyQt4 import QtGui
from PyQt4 import QtCore


class GWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # Set window size, title, icon, statusbar.
        self.setGeometry(10, 10, 1024, 768,)
        self.setWindowTitle('Grasssify')
        self.setWindowIcon(QtGui.QIcon('icon.xpm'))
        self.statusBar().showMessage('Ready')

        # Fill the rest of the window with e.g. text input window
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        
        # Add an file/open menu point
        # Muss irgendwie als erstes kommen, sonst funzt der Scheiß nicht !!!!
        opan = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        opan.setShortcut('Ctrl+O')
        opan.setStatusTip('Open new File')
        self.connect(opan, QtCore.SIGNAL('triggered()'), self.showDialog)
        
        # Add an file/exit menu point
        exit = QtGui.QAction(QtGui.QIcon('exit.svg'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
       
        
        # Add MenuBar 
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        validate = menubar.addMenu('&Validate')
        # Add points for file menu
        file.addAction(opan)
        file.addAction(exit)
        
        # Add points for validate menu
        #validate.addAction()
        
        # Add a shortcut toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exit)
        
    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    '/home')
        file=open(filename)
        data = file.read()
        self.textEdit.setText(data)

      
    # Add small window, asking if you really want to exit
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# main part
app = QtGui.QApplication(sys.argv)
main = GWindow()
main.show()
app.exec_()

