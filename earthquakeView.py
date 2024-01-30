#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
    QSplitter, QStyleFactory, QApplication, QTableView, QGroupBox)
from PyQt5.QtCore import Qt, QAbstractTableModel
import sys
import openGLWindow
import fm, sidePanel
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import os
from platform import system

#from PyQt5.QtWidgets import QDesktopWidget as dw

headers = [ "date", "lat", "lon", "depth", "mag"]


class EarthquakeView(QWidget):

#    data = fm.readData()

    
    def __init__(self):
        super(EarthquakeView, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):      
        self.setWindowTitle("Earthqake View")
        # table max width yparxei gia na mhn xreiazetai na yparxei orizontia mpara gia na doume ta dedomena

        if system() == "Linux":
            #katalhlo platos pinaka gia na mhn emfanizetai orizontia mpara mexri 9999 seismous
            self.tableMaxWidth = 375
            self.setMinimumSize(980, 599)

        else:
            print("WE ARE WINDOWS")
            self.setMinimumSize(930, 599)
            self.tableMaxWidth = 326
        self.dataPath = os.path.expanduser("~/Desktop")
        self.data = []

        hbox = QHBoxLayout()
        hboxButtons = QHBoxLayout()
        vbox = QVBoxLayout()

        self.mapWin = openGLWindow.GLWindow(self)
#        self.mapWin.setData()

        self.fileBtn = QtWidgets.QPushButton("Choose file", self)
        self.chooseBtn = QtWidgets.QPushButton("Sort/Filter", self)
        self.helpBtn = QtWidgets.QPushButton("Color help", self)

        self.ctrlPanel = sidePanel.controlPanel(self)

        self.status = QtWidgets.QStatusBar(self)
        self.status.setSizeGripEnabled(False)
        self.status.setMaximumWidth(self.tableMaxWidth)
        self.status.showMessage("Choose a data file")
        self.earthquakeCount = QtWidgets.QLabel("{} Earthquakes".format(0))#len(self.data)))
        self.status.addPermanentWidget(self.earthquakeCount)

        self.lblFilePath = QtWidgets.QLineEdit("Path: No filepath")
        self.lblFilePath.setMaximumWidth(self.tableMaxWidth)
        self.lblFilePath.setReadOnly(True)

        self.table = QTableView(self)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.model = sidePanel.myTableModel(headers = headers)
        self.table.setModel(self.model)#pm)
        self.table.setMaximumWidth(self.tableMaxWidth)

        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)#stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.table.resizeRowsToContents()

        self.tableBox = QtWidgets.QGroupBox("Earthquake Data", alignment = QtCore.Qt.AlignHCenter)
        self.tableBox.setFlat(True)
        self.tableBox.setMaximumWidth(self.tableMaxWidth)
        helpLayout = QVBoxLayout()
        helpLayout.addWidget(self.table)
        self.tableBox.setLayout(helpLayout)

        hboxButtons.addWidget(self.chooseBtn)
        hboxButtons.addWidget(self.fileBtn)

        vbox.addWidget(self.ctrlPanel)
#        vbox.addWidget(self.fileBtn)
#        vbox.addWidget(self.chooseBtn)
        vbox.addLayout(hboxButtons)
        vbox.addWidget(self.helpBtn)
        vbox.addWidget(self.status)
        vbox.addWidget(self.lblFilePath)
        vbox.addWidget(self.tableBox)

        hbox.addWidget(self.mapWin)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        policy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Expanding, 
        QtWidgets.QSizePolicy.Expanding)
        self.mapWin.setSizePolicy(policy)
        self.table.setSizePolicy(policy)

        self.connectButtonsSignals()

        self.show()


    def chooseFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(None,'Select earthquake dialog', self.dataPath, 'Text files (*.txt) ;; All files (*)')
        if fileName[0]:
            self.dataPath = fileName[0]
            self.lblFilePath.setText(fileName[0])
            self.status.showMessage("Reading data", 0)
            self.data = fm.readData(inputFilename=self.dataPath)

#            print(data)
#            self.status.showMessage("{} Earthquakes".format(len(data)))
            self.earthquakeCount.setText("{} Earthquakes".format(len(self.data)))


            self.mapWin.setData(self.data)

            self.model.clearTable()
        if not self.ctrlPanel.viewMode.isChecked():
            self.model.fillTable(self.data)

    def showChooseDialog(self):
        if len(self.data) == 0:
            self.status.showMessage("No data", self.mapWin.statusMessageTimeout)
            return
        try:
            if not self.dlgChoose.isVisible():
                self.dlgChoose.show()
                self.dlgChoose.activateWindow()
 #               self.dlgChoose.setCurrentWidget()
 #               self.dlgChoose.raise()
 #               print(self.dlgChoose)
        except AttributeError:
            self.dlgChoose = sidePanel.chooseDialog(self)
            # orizoume edw to parakatw signal giati to dlgChoose widget dimiourgeitai edw.
            self.dlgChoose.choiceMade.connect(self.mediator)

    def showHelpDialog(self):
        try:
            if not self.dlgHelp.isVisible():
                self.dlgHelp.show()
                self.dlgHelp.activateWindow()

        except AttributeError:
            self.dlgHelp = sidePanel.helpDialog(self)

    def mediator(self, myFilter):
    # auth h synarthsh pairnei to filtro pou dimiourgise o xristis apo to chooseDialog, to pernaei sth synarthsh fm.choose kai metaferei ta pleon filtrarismena data sto parathyro openGL
#        print("eftasan ta{}".format(myFilter))
#        self.status.showMessage("Filtering data", 0)
        filteredData = fm.choose(self.data, **myFilter)
 #       print("final data {}".format(final))
        self.mapWin.setData(filteredData)
        self.earthquakeCount.setText("{} Earthquakes".format(len(filteredData)))
        self.model.clearTable()
        if not self.ctrlPanel.viewMode.isChecked():
            self.model.fillTable(filteredData)


    def connectButtonsSignals(self):
        self.ctrlPanel.left.clicked.connect(self.mapWin.rotateYleft)
        self.ctrlPanel.right.clicked.connect(self.mapWin.rotateYright)
        self.ctrlPanel.up.clicked.connect(self.mapWin.rotateXleft)
        self.ctrlPanel.down.clicked.connect(self.mapWin.rotateXright)
        self.ctrlPanel.rotLeft.clicked.connect(self.mapWin.rotateZright)
        self.ctrlPanel.rotRight.clicked.connect(self.mapWin.rotateZleft)
        self.ctrlPanel.zoomOut.clicked.connect(self.mapWin.zoomOut)
        self.ctrlPanel.zoomIn.clicked.connect(self.mapWin.zoomIn)
        self.ctrlPanel.center.clicked.connect(self.mapWin.centered)
        self.ctrlPanel.startStop.clicked.connect(self.mapWin.startStop)
        self.ctrlPanel.slow.clicked.connect(self.mapWin.decreaseTimerSpeed)
        self.ctrlPanel.fast.clicked.connect(self.mapWin.increaseTimerSpeed)
        self.ctrlPanel.reverse.clicked.connect(self.mapWin.swapTimelapse)
        # thn epomenh grammh th vazoume giati alliws otan tou kanw click den kanei toggle
        self.ctrlPanel.reverse.clicked.connect(self.ctrlPanel.reverse.toggle)
        self.ctrlPanel.viewMode.toggled.connect(self.mapWin.toggleMode)
        self.mapWin.swapTimelapseSignal.connect(self.ctrlPanel.reverse.toggle)
        self.mapWin.toggleModeSignal.connect(self.toggleviewModeCheckbox)

        # prepei ta signals na exoun ton idio arithmo orismatwn me ta slots pou tha sindethoun
        self.mapWin.proceededTimelapse.connect(self.model.appendRow)#self.model.myFun)
        self.mapWin.proceededTimelapse.connect(self.table.scrollToBottom)
        self.mapWin.rewindedTimelapse.connect(self.model.popRow)
        self.mapWin.sequentialSignal.connect(self.model.clearTable)
        self.mapWin.viewAllSignal.connect(self.model.clearTable)
        self.mapWin.viewAllSignal.connect(self.model.fillTable)

        self.fileBtn.clicked.connect(self.chooseFile)
        self.chooseBtn.clicked.connect(self.showChooseDialog)
        self.helpBtn.clicked.connect(self.showHelpDialog)

        self.mapWin.statusMessage.connect(self.status.showMessage)
        fm.helpSignal.statusMessage.connect(self.status.showMessage)



    def resizeEvent(self, e):
#       self.aspectRatio = 1.5
        print(e.size())#.width())


        # w = e.size().width()
        # h = e.size().height()
        # if w<h:
            # h = w/self.aspectRatio
        # elif w>h:
            # w = h*self.aspectRatio

        # self.resize(w, h)
        pass

    def toggleviewModeCheckbox(self):
        if self.ctrlPanel.viewMode.isChecked():
            self.ctrlPanel.viewMode.setChecked(False)
            self.ctrlPanel.viewMode.toggled.emit(False)

        else:
            self.ctrlPanel.viewMode.setChecked(True)
            self.ctrlPanel.viewMode.toggled.emit(True)

        
if __name__ == '__main__':


    app = QApplication(sys.argv)
    ex = EarthquakeView()
    ex.resize(890, 598)

    
    sys.exit(app.exec_())