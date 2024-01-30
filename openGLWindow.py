from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtOpenGL import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import fm
import os


QtCore.pyqtSignal


class GLWindow(QGLWidget):
#QtWidgets.QOpenGLWidget) den kanoume inherit apo auto giati den doulevei to image. apikonizi mia gri othoni

    #https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    proceededTimelapse = QtCore.pyqtSignal(tuple)
    rewindedTimelapse = QtCore.pyqtSignal()
    sequentialSignal = QtCore.pyqtSignal()
    viewAllSignal = QtCore.pyqtSignal(list)
    statusMessage = QtCore.pyqtSignal(str, int)
    toggleModeSignal = QtCore.pyqtSignal()
    swapTimelapseSignal = QtCore.pyqtSignal()


# bug report: an  valw to data mesa sthn init, leei perierga gia thn metatroph ths hmerominias ton sismon
# bug fixed h domhsh ths hmerominias ginetai tmhmatika anti gia olh mazi dhladh year month day etc kai oxi olh h hmerominia
#    data = fm.readData()

    def __init__(self, parent = None):
        super(GLWindow, self).__init__(parent)

        self.parent = parent
        self.variablesInit()
        args = fm.parseArguments()
#        print(args.sequential)

        if args.file:
            self.sequential = True
            self.data = fm.readData(inputFilename=args.file)
            self.setData(self.data)
#        else:
#            self.data = fm.readData()
            
#        if args.sortBy or args.minDateTime or args.maxDateTime or args.minMag or args.maxMag or args.minLatLon or args.maxLatLon:
#            print("called")
#        self.data = fm.choose(self.data, sortBy=args.sortBy, descending=args.descending, minDate=args.minDate, maxDate=args.maxDate, minMag=args.minMag, maxMag=args.maxMag, minLat=args.minLat, maxLat=args.maxLat, minLon=args.minLon, maxLon=args.maxLon)

        if args.sequential:
            self.sequential = True
            self.sequentialSignal.emit()
        #orizoume to earthquakeIterator -1 gia na mhn mas dixnei kanena seismo sthn arxh
            self.earthquakeIterator = -1
        else:
        #arxikopoioume to sequentiall se true gia na mporei na fortwsei to parathyro xwris na kollisei an yparxoun polloi seismoi
            self.sequential = True
#            self.viewAllSignal.emit(self.data)
            self.earthquakeIterator = -1
            
        if args.verbose:
            self.verbose = True
        else:
            self.verbose = False

#        self.variablesInit()

        if 'self.data' in locals():

            self.setData(self.data)

#       for testFunnc comment also line 772 "self.viewAllSignal.emit(self.data)"
        self.testFunc()


    def variablesInit(self):
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

#        self.earthquakeIterator = 0
        self.lastEarthquake = None
        self.finalColorValue = (0, 1, 0)
        self.newColorValue = (1, 0, 0)
        self.oldColorValue = (0, 0, 1)
        self.dataLength = 0
        
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.rotStep = 3

        self.oldMousePosX = 0 
        self.oldMousePosY = 0

        self.cameraDistanceZ=10
        self.maxCameraDistance = 80
        self.minCameraDistance = 1.5

        self. imageID=0

        self.timerInterval = 1001
        self.statusMessageTimeout = 1000

        self.forwardTimeLapse = True
        # Display in a sequential fashion or all at once
        # used to divide behavior of the mouse click into movement or position display
        self.perspective = False
        # Date - Coords - Depth - Magnitude - Counter
        self.printMask = [True, True, True, True, True]
        self.verboseError = "No verbose output"
        self.timelapseTimer = QtCore.QTimer()
        self.timelapseTimer.timeout.connect(self.proceedTimelapse)
        self.IMAGEFILE = "map.png"

        
    def welcomeMessage(self):
        print("+------------------------------------------------------------------------------+")
        print("| m:Start/Stop\tk-l:Slow/Fast\t\t+-:Zoom In/Zoom Out\t1-5:Print Mask |")
        print("| c:Center Map\to-p:Z Axis Rotation\tarrows:X-Y Axis Rotation               |")
        print("|------------------------------------------------------------------------------|")
        print("| {0} Σεισμοι                                                                    |".format(0))#self.dataLength))
        print("+------------------------------------------------------------------------------+")
        

    def reconnect(self, signal, newhandler=None, oldhandler=None):
        # This functions moves the calback function from the old slot to the new slot
        while True:
            try:
                if oldhandler is not None:
                    signal.disconnect(oldhandler)
                else:
                    signal.disconnect()
            except TypeError:
                break
        if newhandler is not None:
            signal.connect(newhandler)


    def rotateAllAxis(self):
        glRotate(self.xRot, 1, 0, 0)
        glRotate(self.yRot, 0, 1, 0)
        glRotate(self.zRot, 0, 0, 1)


    def proceedTimelapse(self):
        if (self.earthquakeIterator < self.dataLength-1):
            self.earthquakeIterator += 1
#            print("thisi is the data {}".format(self.data))
            self.proceededTimelapse.emit(self.data[self.earthquakeIterator])
        else:
            self.timelapseTimer.stop()
            return

        self.updateGL()


    def rewindTimelapse(self):
        print("iterator before rewind is {}".format(self.earthquakeIterator))
        if self.earthquakeIterator >= 0:
            self.earthquakeIterator -= 1
            self.rewindedTimelapse.emit()
        else:
            self.timelapseTimer.stop()
            return

        self.updateGL()


    def swapTimelapse(self):
        if self.forwardTimeLapse == False:
            self.forwardTimeLapse = True
            self.reconnect(self.timelapseTimer.timeout, self.proceedTimelapse, self.rewindTimelapse)
            print("Forward timelapse")
            self.statusMessage.emit("Forward timelapse", self.statusMessageTimeout)
        else:
            self.forwardTimeLapse = False
            self.reconnect(self.timelapseTimer.timeout, self.rewindTimelapse, self.proceedTimelapse)
            print("Rewind timelapse")
            self.statusMessage.emit("Rewind timelapse", self.statusMessageTimeout)
        self.swapTimelapseSignal.emit()


    def paintGL(self):
#        print("Iterator:{}".format(self.earthquakeIterator))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(0.33, 0.33, 0.33)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.rotateAllAxis()

#        glRectd(-10, -10, 10, 10) # Test rectangle.

# https://www.opengl.org/discussion_boards/showthread.php/178630-Texture-Changes-Color
        glEnable(GL_TEXTURE_2D)
        self.textureBox()
        glDisable(GL_TEXTURE_2D)

        #an to epipedo einai gyrismeno kata 90 moires ws pros x tote  emfanise mia gramh pou symvolizei ton orizonta
        if abs(self.xRot) > 87 and abs(self.xRot) < 92:
            glBegin(GL_LINES)
            glVertex3fv((-20, 0, 0))
            glVertex3fv((20, 0, 0))
            glEnd()

            glBegin(GL_LINES)
            glVertex3fv((0,-20, 0))
            glVertex3fv((0, 20, 0))
            glEnd()

        if (self.sequential):
            self.sequentialDraw()
        else:
            self.viewAllDraw()


    def setPerspectiveProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        w = self.width()
        h = self.height()
#        print("width is {} \nheight is {}".format(w, h))
        gluPerspective(90.0, w/h, 1, 80)
        gluLookAt(0,0,self.cameraDistanceZ, 0,0, -10, 0,1,0)
        self.perspective = True
        self.setMouseTracking(False)
        self.setWindowTitle("Earthquake View")


    def setOrthoProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10, 10, -10, 10, -5.0, 25.0)
        gluLookAt(0,0,self.cameraDistanceZ, 0,0, -10, 0,1,0)
        self.perspective = False
        self.setMouseTracking(True)


    # Keep angle in the range 0 - 360
    def normalizeAngle(self, angle):
        if angle>359:
            angle -= 360
        elif angle<-359:
            angle += 360

        return angle


    def rotateXright(self):
        self.xRot += self.rotStep
        self.xRot = self.normalizeAngle(self.xRot)
        if self.xRot != 0:
            self.setPerspectiveProjection()

        self.updateGL()


    def rotateXleft(self):
        self.xRot -= self.rotStep
        self.xRot = self.normalizeAngle(self.xRot)
        if self.xRot != 0:
            self.setPerspectiveProjection()

        self.updateGL()


    def rotateYright(self):
        self.yRot += self.rotStep
        self.yRot = self.normalizeAngle(self.yRot)
        if self.yRot != 0:
            self.setPerspectiveProjection()

        self.updateGL()


    def rotateYleft(self):
        self.yRot -= self.rotStep
        self.yRot = self.normalizeAngle(self.yRot)
        if self.yRot != 0:
            self.setPerspectiveProjection()

        self.updateGL()


    def rotateZright(self):
        self.zRot += self.rotStep
        self.zRot = self.normalizeAngle(self.zRot)
        if self.zRot != 0:
            self.setPerspectiveProjection()

        self.updateGL()


    def rotateZleft(self):
        self.zRot -= self.rotStep
        self.zRot = self.normalizeAngle(self.zRot)
        if self.zRot != 0:
            self.setPerspectiveProjection()

        self.updateGL()


    def resizeGL(self, w, h):
#        print("Resize loop")
        if w<h:
            h = w
        elif h<w:
            w = h
        self.resize(w,h)
        glViewport(0, 0, w, h)
        if self.perspective:
            self.setPerspectiveProjection()
        else:
            self.setOrthoProjection()
#        print("GL:{}\nW:{}\nH:{}".format(self.size(), w, h))

#        print("Error:",  glGetError())


    def initializeGL(self):
#        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#        glEnable( GL_BLEND )
#        glEnable(GL_DEPTH_TEST)
        glClearColor(0.65, 0.65, 0.65, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)# | GL_DEPTH_BUFFER_BIT)
#        glClearDepth(1.0)
        self.imageID = self.LoadImage()
        self.setupTexture()
#        print("Error:",  glGetError())
#        self.glutInitialization()
        self.updateGL()
        self.welcomeMessage()
        

    def glutInitialization(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(315, 100)
        glutCreateWindow(b"Close to terminate earthquake view")
        glutHideWindow()


    def keyPressEvent(self, e):
#        print("key pressed", e.text())
        if e.isAutoRepeat():
            return

        if e.key() == QtCore.Qt.Key_Escape:
             QtWidgets.QApplication.closeAllWindows()

        elif e.key() == QtCore.Qt.Key_Up:
            self.rotateXleft()

        elif e.key() == QtCore.Qt.Key_Down:
            self.rotateXright()

        elif e.key() == QtCore.Qt.Key_Left:
            self.rotateYleft()

        elif e.key() == QtCore.Qt.Key_Right:
            self.rotateYright()

        elif e.key() == QtCore.Qt.Key_O:
            self.rotateZright()
            
        elif e.key() == QtCore.Qt.Key_P:
            self.rotateZleft()            

        elif e.key() == QtCore.Qt.Key_C:
            self.centered()

        #timer start/stop
        elif e.text() == "m":
            self.startStop()

        elif e.key() == QtCore.Qt.Key_N:
            self.swapTimelapse()

        elif e.key() == QtCore.Qt.Key_K:
            self.decreaseTimerSpeed()

        elif e.key() == QtCore.Qt.Key_L:
            self.increaseTimerSpeed()

        elif e.key() == QtCore.Qt.Key_T:
            # this signal is emited to update the side panel
            self.toggleModeSignal.emit()
            self.toggleMode()

        elif e.key() == QtCore.Qt.Key_Minus:
            self.zoomOut()

        elif e.key() == QtCore.Qt.Key_Plus:
            self.zoomIn()

        elif e.key() == QtCore.Qt.Key_1:
            if self.verbose:
                if self.printMask[0]:
                    print("Date Disabled")
                else:
                    print("Date Enabled")
                self.printMask[0] = not self.printMask[0]
            else:
                print(self.verboseError)
                
        elif e.key() == QtCore.Qt.Key_2:
            if self.verbose:
                if self.printMask[1]:
                    print("Coords Disabled")
                else:
                    print("Coords Enabled")
                self.printMask[1] = not self.printMask[1]
            else:
                print(self.verboseError)

        elif e.key() == QtCore.Qt.Key_3:
            if self.verbose:

                if self.printMask[2]:
                    print("Depth Disabled")
                else:
                    print("Depth Enabled")
                self.printMask[2] = not self.printMask[2]
            else:
                print(self.verboseError)

        elif e.key() == QtCore.Qt.Key_4:
            if self.verbose:
                if self.printMask[3]:
                    print("Date Disabled")
                else:
                    print("Date Enabled")
                self.printMask[3] = not self.printMask[3]
            else:
                print(self.verboseError)

        elif e.key() == QtCore.Qt.Key_5:
            if self.verbose:
                if self.printMask[4]:
                    print("Counter Disabled")
                else:
                    print("Counter Enabled")
                self.printMask[4] = not self.printMask[4]
            else:
                print(self.verboseError)
                

    def mouseMoveEvent(self, e):
#        print("Mouse position is {}".format(e.pos()))
        if not self.perspective:
            # Check if the mouse is within the window borders
            if 0 <= e.x() <= self.width() and 0 <= e.y() <= self.height():
                coords = fm.windowToLatLon(self.width(), self.height(), e.x(), e.y())

                if self.parent is None:
                    self.setWindowTitle("Earthquake View   ({0:.2f} {1:.2f})".format(coords[0], coords[1]))
                else:
#                    print(self.rect())
                    self.parent.setWindowTitle("Earthquake View   ({0:.2f} {1:.2f})".format(coords[0], coords[1]))

            #print(fm.windowToLatLon(self.width(), self.height(), e.x(), e.y()))
            #print("Mouse pos {}".format(e.pos()))
            return

        if e.x() > self.oldMousePosX:
            self.rotateYright()
        elif e.x() < self.oldMousePosX:
            self.rotateYleft()

        if e.y() > self.oldMousePosY:
            self.rotateXright()
        elif e.y() < self.oldMousePosY:
            self.rotateXleft()

        self.oldMousePosX = e.x()
        self.oldMousePosY = e.y()
        return


    def mousePressEvent(self, e):
#        print(e.button)
        if e.button() == QtCore.Qt.RightButton:
            self.centered()
        elif e.button() == QtCore.Qt.LeftButton:
            if  not self.perspective:
                self.setPerspectiveProjection()
                if self.parent:
                    self.parent.setWindowTitle("Earthquake View")
                else:
                    self.setWindowTitle("Earthquake View")


    def wheelEvent(self, e):
#        print("here is wheel event {}".format(e.angleDelta().y()))
        delta = e.angleDelta().y()
        if delta > 0:
#            print("called zoomIN")
            self.zoomIn()
        else:
#            print("called zoomOUT")
            self.zoomOut()


    def zoomIn(self):
        print(self.cameraDistanceZ)
        if self.cameraDistanceZ == self.minCameraDistance:
            self.statusMessage.emit("Minimum distance reached", self.statusMessageTimeout) 
            return
        self.cameraDistanceZ -= 0.5
        # Prepei na kaloume opwsdipote thn setPerspectiveProjection giati doulevoun oles oi synartiseis ths gia na ginei to zoom
        self.setPerspectiveProjection()
        self.updateGL()


    def zoomOut(self):
        if self.cameraDistanceZ == self.maxCameraDistance:
            self.statusMessage.emit("Maximum distance reached", self.statusMessageTimeout) 
            return

        self.cameraDistanceZ += 0.5

        self.setPerspectiveProjection()
        self.updateGL()


    def centered(self):
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.cameraDistanceZ = 10
        self.setOrthoProjection()
        self.updateGL()


    def toggleTimer(self, timer):
        if timer.isActive():
            timer.stop()
            print("Timer stopped")
            self.statusMessage.emit("Timer stopped", self.statusMessageTimeout) 

        else:
            timer.start(self.timerInterval)
            print("Timer started")
            self.statusMessage.emit("Timer started", self.statusMessageTimeout) 


    def increaseTimerSpeed(self):
        if self.timerInterval > 250:
            self.timerInterval -= 250

            if self.timelapseTimer.isActive():
                self.timelapseTimer.start(self.timerInterval)

            print("Timer interval is {}ms".format(self.timerInterval))
            self.statusMessage.emit("Timer interval is {}ms".format(self.timerInterval), self.statusMessageTimeout) 
        else:
            self.statusMessage.emit("Minimum interval reached", self.statusMessageTimeout)


    def decreaseTimerSpeed(self):
        if self.timerInterval < 1000:
            self.timerInterval += 250

            if self.timelapseTimer.isActive():
                self.timelapseTimer.start(self.timerInterval)
            self.statusMessage.emit("Timer interval is {}ms".format(self.timerInterval), self.statusMessageTimeout)

        else:
            self.statusMessage.emit("Maximum interval reached", self.statusMessageTimeout)


    def textureBox(self):
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-10.0, -10.0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(10.0, -10.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(10.0, 10.0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(10.0, 10.0)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(-10.0, 10.0)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-10.0, -10.0)
        glEnd()


    def LoadImage(self):
        #den doulevei auth h if
        if not QtCore.QFileInfo.exists(self.IMAGEFILE):
            print("file {} does not exists.".format(self.IMAGEFILE))
            QtWidgets.QApplication.closeAllWindows()#self.quit(1)

        imga = QtGui.QImage(self.IMAGEFILE)
        imga = imga.convertToFormat(QtGui.QImage.Format_RGB888)
        img = imga.mirrored()
        width = img.width()
        height = img.height()

        # an vgazei provlima me ton ptr, pithanws den yparxei to img
        ptr = img.bits()
        ptr.setsize(img.byteCount())
        data = ptr.asstring()

        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
#        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
#        print("paketo")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_BGR, GL_UNSIGNED_BYTE, data)
#        print("ola koble")

#        print("ID =", ID)
        return ID


    def setupTexture(self):
        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

#        glBindTexture(GL_TEXTURE_2D, self.imageID)
#        print("Error:",  glGetError())


    def sequentialDraw(self):
        #orizoume to earthquakeIterator -1 gia na mhn mas dixnei kanena seismo sthn arxh
        if self.earthquakeIterator == -1:
            if not self.forwardTimeLapse:
                self.statusMessage.emit("Begining of data reached.", 0)

#            print("seqData\n\n{}".format(self.data))
            return

        for d in self.dataToPaint[:self.earthquakeIterator]:
        #data to paint format is a list of [x, y, z, color(tuple)]
            self.positioning(d[:-1])
            glColor3f(*d[-1])
            self.drawOctahedron(0.08)#glutWireSphere(0.05, 20, 20)


#        print("SEQUENTIALDATA\n\n{}".format(self.data[:self.earthquakeIterator]))
        newSismos = self.dataToPaint[self.earthquakeIterator]
        self.positioning(newSismos[:-1])

        # if this is the last earthquake paint green else red.
        if self.earthquakeIterator == self.dataLength -1:
            glColor3f(*self.finalColorValue)
   #         print("iterator is {} total is {}".format(self.earthquakeIterator, self.dataLength))
            self.statusMessage.emit("End of data reached.", 0)
        else:
            glColor3f(*self.newColorValue)

        self.drawOctahedron(0.1)#glutWireSphere(0.1, 20, 20)
        
        
        if (self.verbose and (self.lastEarthquake != newSismos)): # auto to && ginetai gia na min emfanizei sinexia sto command line ta stoixia tou
            self.lastEarthquake = newSismos                    # teleutaiou sismou otan peristrefoume to xarth
            self.printInfo(newSismos)


    def viewAllDraw(self):
        for d in self.dataToPaint:
        #data to paint format is a list of [x, y, z, color(tuple)]
            self.positioning(d[:-1])
            glColor3f(*d[-1])

            self.drawOctahedron(0.08)
#            glutWireSphere(0.05, 20, 20)


    def positioning(self, d):
        x, y, z = d
        glLoadIdentity()
        self.rotateAllAxis()
        glTranslate(x, y, -z)


    def colorDefinition(self, depth):
        red = 0# mag/8
        blue = 1
        green = float(format(depth/25, '.3f'))#3*depth/20
#        print("depth={} green={}".format(depth, green))
#        glColor3f(red, green, blue)
        return (red, green, blue)


    def calcXYZColor(self, data):
        dataToPaint= []
        for d in data:
            lat, lon, depth = d[1:-1]
            myX, myY = fm.latLonToCart(lat, lon)  
            color = self.colorDefinition(depth/10)
            # ypodekaplasiazoume to depth giati oi apokleiseis stin eikona einai poly megales 
            dataToPaint.append([myX, myY, depth/10, color])
#        print("DATA TO SHOW\n{}".format(dataToPaint))
        return dataToPaint


    def printInfo(self, sismos):
        date, lat, lon, depth, mag = sismos
        if self.printMask[0]:
            print("Date:{0}".format(date), end=" ")
        if self.printMask[1]:
            print("Lat:{0} Lon:{1}".format(lat, lon), end=" ")
        if self.printMask[2]:
            print("Depth:{0}".format(depth), end=" ")
        if self.printMask[3]:
            print("Magnitude:{0}".format(mag), end=" ")
        if self.printMask[4]:
            print("{0} of {1}".format(self.earthquakeIterator + 1, self.dataLength))
        print()


    #kaleitai otan to pontiki feugei apo to widget
    def leaveEvent(self, event):
        if self.parent is None:
            self.setWindowTitle("Earthquake View")
        else:
            self.parent.setWindowTitle("Earthquake View")


    def setData(self, newData):
        self.dataLength = len(newData)
        print("Sismoi:{}".format(self.dataLength))
        if not self.sequential:
            self.viewAllSignal.emit(newData)

        else:
            if self.timelapseTimer:
                self.timelapseTimer.stop()
            self.earthquakeIterator = -1

        self.data = newData
        self.dataToPaint = self.calcXYZColor(newData)
        self.statusMessage.emit("Data acquired", 0)

        
        self.updateGL()


    def startStop(self):
        if self.dataLength == 0:
            self.statusMessage.emit("No data", self.statusMessageTimeout)
            return
        if not self.sequential:
            print("You are in View all mode")
            self.statusMessage.emit("You are in View all mode.", self.statusMessageTimeout) 
            return

        else:

            if self.forwardTimeLapse:
                if self.earthquakeIterator == self.dataLength -1:
                    self.statusMessage.emit("End of data reached.", self.statusMessageTimeout)
                    return
            else:
                if self.earthquakeIterator == -1:
                    self.statusMessage.emit("Begining of data reached.", self.statusMessageTimeout) 
                    return

        self.toggleTimer(self.timelapseTimer)


    def toggleMode(self):
        if self.dataLength == 0:
            self.statusMessage.emit("No data", self.statusMessageTimeout)
            return
        if self.sequential:
            self.timelapseTimer.stop()
#            self.viewAllSignal.emit(self.data)
            self.statusMessage.emit("Show all mode", self.statusMessageTimeout) 

        else:
            self.sequentialSignal.emit()
            self.earthquakeIterator = -1
            self.statusMessage.emit("Sequential mode", self.statusMessageTimeout) 

        self.sequential = not self.sequential
        self.updateGL()


    def testFunc(self):
        self.dataToPaint = []
        self.dataLength = 21
        for x in range(-10, 11):
            depth = x*x
#            self.dataToPaint.append([x, x, depth/10, self.colorDefinition(depth/10)])
            self.dataToPaint.append([x, 0, depth/10, self.colorDefinition(depth/10)])

    def drawOctahedron(self, radius):

        topBottom = ((0, radius, 0), (0, -radius, 0))
        sides = ((radius, 0, 0), (0, 0, radius), (-radius, 0, 0), (0, 0, -radius), (radius, 0, 0))


        for edge in topBottom:
            glBegin(GL_TRIANGLE_FAN)#GL_TRIANGLE_STRIP)
            glVertex3fv(edge)
            for side in sides:
                glVertex3fv(side)
            glEnd()
        


def main():
    app = QtWidgets.QApplication(["Earthquake View"])
    widget = GLWindow()
    widget.show()
    sys.exit(app.exec_())
        

if __name__ == '__main__':
    main()