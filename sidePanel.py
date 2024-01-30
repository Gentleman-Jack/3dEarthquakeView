#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox,QLineEdit,QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QRegExpValidator
import sys, os
from PyQt5.QtCore import Qt, QAbstractTableModel




class chooseDialog(QtWidgets.QDialog):
    sortList = ["Date", "Latitude", "Longtitude", "Depth", "Magnitude", "Do not sort"]
    choices = {}
    choiceMade = QtCore.pyqtSignal(dict)


    def __init__(self, parent = None):
        super(chooseDialog, self).__init__(parent)
        self.setUI()


    def setUI(self):
        self.setWindowTitle("Sort/Filter")



#        print("ksekiname thn init")
        self.comboSort = QComboBox(self)
        self.comboSort.addItems(self.sortList)
        self.comboSort.currentIndexChanged.connect(self.sortingPreference)

        self.comboOrder = QComboBox(self)
        self.comboOrder.addItems(["Ascending", "Descending"])
        self.comboOrder.currentIndexChanged.connect(self.sortingOrder)

        # auth h grammh prepei na mpei afou exei dhmiourgithei to comboOrder
        self.comboSort.setCurrentIndex(5)



        dblValidator = QDoubleValidator(0.0, 99.99, 2, self)
        dblValidator.setNotation(0)# 0=Standard Notation - 1=Scientific Notation

        magValidator = QDoubleValidator(0.0, 10.0, 1, self)
        magValidator.setNotation(0)# 0=Standard Notation - 1=Scientific Notation


        self.dateMin = QLineEdit(self)
        self.dateMin.textChanged.connect(self.setDateMin)
        self.dateMin.setPlaceholderText("dd/mm/yyyy")

        self.dateMax = QLineEdit(self)
        self.dateMax.textChanged.connect(self.setDateMax)

        self.latMin = QLineEdit(self)
        self.latMin.textChanged.connect(self.setLatMin)
        self.latMin.setPlaceholderText("float")
        self.latMin.setValidator(dblValidator)

        self.latMax = QLineEdit(self)
        self.latMax.textChanged.connect(self.setLatMax)
        self.latMax.setValidator(dblValidator)

        self.lonMin = QLineEdit(self)
        self.lonMin.textChanged.connect(self.setLonMin)
        self.lonMin.setPlaceholderText("float")
        self.lonMin.setValidator(dblValidator)


        self.lonMax = QLineEdit(self)
        self.lonMax.textChanged.connect(self.setLonMax)
        self.lonMax.setValidator(dblValidator)

        self.depthMin = QLineEdit(self)
        self.depthMin.setPlaceholderText("int")
        self.depthMin.setValidator(QIntValidator (0, 300))
        self.depthMin.textChanged.connect(self.setDepthMin)

        self.depthMax = QLineEdit(self)
        self.depthMax.textChanged.connect(self.setDepthMax)
        self.depthMax.setValidator(QIntValidator (0, 300))

        self.magMin = QLineEdit(self)
        self.magMin.textChanged.connect(self.setMagMin)
        self.magMin.setPlaceholderText("float")
        self.magMin.setValidator(magValidator)

        self.magMax = QLineEdit(self)
        self.magMax.textChanged.connect(self.setMagMax)
        self.magMax.setValidator(magValidator)

        self.total = QLineEdit(self)
        self.total.textChanged.connect(self.setTotal)
        self.total.setValidator(QIntValidator (0, 999999))

        self.emptylabel = QLabel("",self)
        self.lblSortBy = QLabel("Sorting preference", self)
        self.lblSortBy.setAlignment(QtCore.Qt.AlignRight)
        self.lblDate = QLabel("Date  dd/mm/yyyy", self)
        self.lblDate.setAlignment(QtCore.Qt.AlignRight)
        self.lblLat = QLabel("Latitude       xx.xx", self)
        self.lblLat.setAlignment(QtCore.Qt.AlignRight)
        self.lblLon = QLabel("Longtitude   xx.xx", self)
        self.lblLon.setAlignment(QtCore.Qt.AlignRight)
        self.lblDepth = QLabel("Depth (Km)      xxx", self)
        self.lblDepth.setAlignment(QtCore.Qt.AlignRight)
        self.lblMag = QLabel("Magnitude  Richter", self)
        self.lblMag.setAlignment(QtCore.Qt.AlignRight)
        self.lblMax = QLabel("Max", self)
        self.lblMin = QLabel("Min", self)
        self.lblOrder = QLabel("Sorting order")
        self.lblTotal = QLabel("Total amount")

        self.okBtn = QtWidgets.QPushButton("OK", self)
        self.okBtn.setDefault(True)
        self.okBtn.clicked.connect(self.accept)

        self.cancelBtn = QtWidgets.QPushButton("Cancel", self)
        self.cancelBtn.clicked.connect(self.reject)

        self.grid = QGridLayout()

        #first column
        self.grid.addWidget(self.lblDate, 1, 0)
        self.grid.addWidget(self.lblLat, 2, 0)
        self.grid.addWidget(self.lblLon, 3, 0)
        self.grid.addWidget(self.lblDepth, 4, 0)
        self.grid.addWidget(self.lblMag, 5, 0)
        self.grid.addWidget(self.lblSortBy, 6, 0)
        self.grid.addWidget(self.lblOrder, 7, 0)
        self.grid.addWidget(self.lblTotal, 8, 0)

        #second column
        self.grid.addWidget(self.lblMin, 0, 1)
        self.grid.addWidget(self.dateMin, 1, 1)
        self.grid.addWidget(self.latMin, 2, 1)
        self.grid.addWidget(self.lonMin, 3, 1)
        self.grid.addWidget(self.depthMin, 4, 1)
        self.grid.addWidget(self.magMin, 5, 1)
        self.grid.addWidget(self.emptylabel, 6, 1)
        self.grid.addWidget(self.emptylabel, 7, 1)
        self.grid.addWidget(self.emptylabel, 8, 1)

        #third column
        self.grid.addWidget(self.lblMax, 0, 2)
        self.grid.addWidget(self.dateMax, 1, 2)
        self.grid.addWidget(self.latMax, 2, 2)
        self.grid.addWidget(self.lonMax, 3, 2)
        self.grid.addWidget(self.depthMax, 4, 2)
        self.grid.addWidget(self.magMax, 5, 2)
        self.grid.addWidget(self.comboSort, 6, 2)
        self.grid.addWidget(self.comboOrder, 7, 2)
        self.grid.addWidget(self.total, 8, 2)

        self.grid.addWidget(self.okBtn, 9, 2)
        self.grid.addWidget(self.cancelBtn, 9, 1)

        self.setLayout(self.grid)
        self.show()
#        print("teleiwsame thn init")


        if self.choices:
            for k,v in self.choices.items():
                if k == "minDate":
                    self.dateMin.setText(str(v))
                if k == "maxDate":
                    self.dateMax.setText(str(v))
                if k == "minLat":
                    self.latMin.setText(str(v))
                if k == "maxLat":
                    self.latMax.setText(str(v))
                if k == "minLon":
                    self.lonMin.setText(str(v))
                if k == "maxLon":
                    self.lonMax.setText(str(v))
                if k == "minDepth":
                    self.depthMin.setText(str(v))
                if k == "maxDepth":
                    self.depthMax.setText(str(v))
                if k == "minMag":
                    self.magMin.setText(str(v))
                if k == "maxMag":
                    self.magMax.setText(str(v))
                if k == "descending":
                    self.comboOrder.setCurrentIndex(v)
                if k == "sortBy":
                    self.comboSort.setCurrentIndex(v)
                if k == "total":
                    self.total.setText(str(v))

        self.setFixedSize(self.size())


    def setDateMin(self, dateMin):
        try:
            self.choices["minDate"] = dateMin
        except:
            print("unable to convert")


    def setDateMax(self, dateMax):

        self.choices["maxDate"] = dateMax


    def setLatMin(self, latMin):
        try:
            self.choices["minLat"] = float(latMin)
        except:
            del self.choices["minLat"]


    def setLatMax(self, latMax):
        try:
            self.choices["maxLat"] = float(latMax)
        except:
            del self.choices["maxLat"]


    def setLonMin(self, lonMin):
        try:
            self.choices["minLon"] = float(lonMin)
        except:
            del self.choices["minLon"]


    def setLonMax(self, lonMax):
        try:
            self.choices["maxLon"] = float(lonMax)
        except:
            del self.choices["maxLon"]


    def setDepthMin(self,depthMin):
        try:
            self.choices["minDepth"] = int(depthMin)
        except:
            del self.choices["minDepth"]


    def setDepthMax(self, depthMax):
        try:
            self.choices["maxDepth"] = int(depthMax)
        except:
            del self.choices["maxDepth"]


    def setMagMin(self, magMin):
        try:
            self.choices["minMag"] = float(magMin)
        except:
            del self.choices["minMag"]


    def setMagMax(self, magMax):
#        print("MagMax = {}\nFloatValue = {}".format(magMax,float(magMax)))
        try:
            self.choices["maxMag"] = float(magMax)
        except:
            del self.choices["maxMag"]


    def sortingPreference(self, e):
        print(e)
        self.choices["sortBy"] = e
        if e == 5:
            self.comboOrder.setDisabled(True)
        else:
            self.comboOrder.setDisabled(False)


    def sortingOrder(self, e):
        print(e)
        self.choices["descending"] = bool(e)

    def setTotal(self, total):
        try:
            self.choices["total"] = int(total)
        except:
            del self.choices["total"]


    def accept(self):
#        print(self.choices)
        self.choiceMade.emit(self.choices)
        self.done(1)



class controlPanel(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(controlPanel, self).__init__(parent)
        self.setUI()


    def setUI(self):
        self.ctrl = QtWidgets.QGroupBox("Navigation", alignment = QtCore.Qt.AlignHCenter)
        self.viewMode = QtWidgets.QGroupBox("Enabled: Sequential View - Disabled: View All")
        self.viewMode.setCheckable(True)

        self.left = QtWidgets.QPushButton("left", self, autoRepeat=True)
        self.right = QtWidgets.QPushButton("right", self, autoRepeat=True)
        self.up = QtWidgets.QPushButton("up", self, autoRepeat=True)
        self.down = QtWidgets.QPushButton("down", self, autoRepeat=True)
        self.rotRight = QtWidgets.QPushButton("rotRight", self, autoRepeat=True)
        self.rotLeft = QtWidgets.QPushButton("rotLeft", self, autoRepeat=True)
        self.zoomOut = QtWidgets.QPushButton("zoom out", self, autoRepeat=True)
        self.zoomIn = QtWidgets.QPushButton("zoom in", self, autoRepeat=True)
        self.center = QtWidgets.QPushButton("center",self)
        self.startStop = QtWidgets.QPushButton("start/stop", self)
        self.slow = QtWidgets.QPushButton("slower", self)
        self.fast = QtWidgets.QPushButton("faster", self)
        self.reverse = QtWidgets.QPushButton("reverse timelapse", self)
        self.reverse.setCheckable(True)

        self.grid = QGridLayout()
        self.grid1 = QGridLayout()


        self.grid.addWidget(self.rotLeft, 0, 0)
        self.grid.addWidget(self.up, 0, 1)
        self.grid.addWidget(self.rotRight, 0, 2)
        self.grid.addWidget(self.left, 1, 0)
        self.grid.addWidget(self.down, 1, 1)
        self.grid.addWidget(self.right, 1, 2)
        self.grid.addWidget(self.zoomOut, 2, 0)
        self.grid.addWidget(self.center, 2, 1)
        self.grid.addWidget(self.zoomIn, 2, 2)

        self.ctrl.setLayout(self.grid)


        self.grid1.addWidget(self.startStop, 0, 0, 1, 2)
        self.grid1.addWidget(self.slow, 1, 0)
        self.grid1.addWidget(self.fast, 1, 1)
        self.grid1.addWidget(self.reverse, 2, 0, 1, 2)

        self.viewMode.setLayout(self.grid1)

        v = QVBoxLayout()
        v.addWidget(self.ctrl)
        v.addWidget(self.viewMode)
        self.setLayout(v)


class myTableModel(QtCore.QAbstractTableModel):

    def __init__(self, data = [], headers = [], parent = None):
        super(myTableModel, self).__init__(parent)
        self.data = data
        self.headers = headers


    def rowCount(self, parent):
        return len(self.data)


    def columnCount(self, parent):
        return len(self.headers)


    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()

            if column == 0:
#                print("provlima me ta panta: {} {}".format(len(self.data[0]), self.data[0] ))
                value =self.data[row][column].strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = self.data[row][column]
            return value

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter


    def flags(self, index):
       return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            elif orientation == Qt.Vertical:
                return section + 1


    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), data=(None, None, None, None, None)):
        self.beginInsertRows( parent, position, position + rows -1)
        if rows > 1:
#            print("LAST STEP BEFORE INSERT\n{}".format(data))
            for i in range(rows):
#                print("NOW INSERT THIS LINE\n{}".format(data[i]))
                self.data.insert(position + rows -1 ,data[i])
        else:
            self.data.insert(position,data)

        self.endInsertRows()
        return True


    def removeRows(self, position, rows, parent =QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows -1)
        for i in range(rows):
            value = self.data[position]
            self.data.remove(value)

        self.endRemoveRows()
        return True


    def appendRow(self,newData):
 #       print("called {}".format(newData))
        self.insertRows(len(self.data), 1, data=newData)


    def popRow(self):
#        print("pop row {}".format(len(self.data)))
        self.removeRows(len(self.data) -1, 1)


    def fillTable(self, newData):
#        print("DATA TO FILL FULL TABLE\n{}".format(newData))
        self.insertRows(0, len(newData), data=newData)


    def clearTable(self):
        self.removeRows(0, len(self.data))
        return True


#http://www.qtcentre.org/archive/index.php/t-61220.html
#if your model is not used with a different proxy in a second view, it might be worth considering implementing the filter in the model itself.
class SequentialProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(SequentialProxyModel, self).__init__()
        self.setDynamicSortFilter(True)


    def filterAcceptsRow(self, row, parent):
        sourceModel=self.sourceModel()
        print("row is {}, iterator is {}".format(row, sourceModel.earthquakeIterator))
        print("data{}".format(sourceModel.data))
        return row <= sourceModel.earthquakeIterator

class helpDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(helpDialog, self).__init__(parent)

        self.setUI()

    def setUI(self):
        self.setWindowTitle("Color Help")
        pxBar = QtGui.QPixmap("colorBar.png")
        pxBar = pxBar.scaled(pxBar.width(),pxBar.height()/3, aspectRatioMode = QtCore.Qt.IgnoreAspectRatio)
        pxRed = QtGui.QPixmap(25, 25)
        pxRed.fill(QtCore.Qt.red)

        #failed rotation
#        pxRed = pxRed.scaled(pxRed.width()*1.414, pxRed.height()*1.414, aspectRatioMode = QtCore.Qt.IgnoreAspectRatio)
#        transformation = QtGui.QTransform()
#        pxRed = pxRed.transformed(transformation.rotate(-45))

        pxGreen = QtGui.QPixmap(25, 25)
        pxGreen.fill(QtCore.Qt.green)
        lblBar = QLabel() 
        lblBar.setPixmap(pxBar)
        lblBar.setSizePolicy( QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred )
        lblRed = QLabel()
        lblRed.setPixmap(pxRed)

        lblGreen = QLabel()
        lblGreen.setPixmap(pxGreen)

        txtRed = QLabel("Newest")#\nearthquake")
        txtGreen = QLabel("Last")#\nearthquake")

        sequentialGroup= QtWidgets.QGroupBox(" Sequential View", alignment = QtCore.Qt.AlignHCenter)

        #1st setup
        grid = QGridLayout()
        grid.addWidget(txtRed, 0, 0)
        grid.addWidget(txtGreen, 0, 1)
        grid.addWidget(lblRed, 1, 0)
        grid.addWidget(lblGreen, 1, 1)

        #2nd setup
        v3 = QVBoxLayout()
        v3.addWidget(txtRed)
        v3.addWidget(lblRed)
        v3.addWidget(txtGreen)
        v3.addWidget(lblGreen)
        sequentialGroup.setLayout(v3)#grid)

        v2 = QVBoxLayout()
        v2.addWidget(QLabel("    0 km"))
        v2.addWidget(QLabel("  50 km"))
        v2.addWidget(QLabel("100 km"))
        v2.addWidget(QLabel("150 km"))
        v2.addWidget(QLabel("200 km"))
        v2.addWidget(QLabel("250 km"))

        grid2 = QGridLayout()
        grid2.addWidget(lblBar, 0,1)
        grid2.addLayout(v2, 0,0)
#        grid2.setHorizontalSpacing(grid2.horizontalSpacing()/2)
#        grid2.addWidget(QLabel("0 Km"), 0,1,0,1)
        
        v = QVBoxLayout()
        v.addWidget(lblBar)
        v.addWidget(sequentialGroup) 

        h = QHBoxLayout()
        h.addLayout(grid2)
        h.addWidget(sequentialGroup)#grid)
        self.setLayout(h)#grid2)
        self.show()

#        self.setFixedSize(self.size())

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
#    ex = chooseDialog()
#    ex = controlPanel()
    ex = helpDialog()
    ex.show()
#    print("dosame to paron")

    sys.exit(app.exec_())