# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application ad then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

from PyQt5.QtWidgets import QApplication, QMainWindow,QAction, QFileDialog, QMessageBox, QSlider, QComboBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QPixmap
import sys
from PyQt5.QtCore import Qt, QPoint

class PaintingApplication(QMainWindow): # documentation https://doc.qt.io/qt-5/qmainwindow.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Paint Application")

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        #set the icon
        # windows version
        self.setWindowIcon(QIcon("./icons/paint-brush.png")) # documentation: https://doc.qt.io/qt-5/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # image settings (default)
        self.image = QImage(self.size(), QImage.Format_RGB32) # documentation: https://doc.qt.io/qt-5/qimage.html#QImage-1
        self.image.fill(Qt.white) # documentation: https://doc.qt.io/qt-5/qimage.html#fill-1

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black # documenation: https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html
        self.brushType=Qt.SolidLine
        self.brushCap=Qt.RoundCap
        self.brushJoin=Qt.RoundJoin

        # reference to last point recorded by mouse
        self.lastPoint = QPoint() # documenation: https://doc.qt.io/qt-5/qpoint.html

        # set up menus
        mainMenu = self.menuBar() # create and a menu bar
        fileMenu = mainMenu.addMenu(" File") # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size") # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(" Brush Color") # add the "Brush Colour" menu to the menu bar
        helpMenu = mainMenu.addMenu("Help")

        #open
        openAction = QAction(QIcon("./icons/open.png"), "Open", self)
        openAction.setShortcut("Ctrl+O")
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save", self)   # create a save action with a png as an icon, documenation: https://doc.qt.io/qt-5/qaction.html
        saveAction.setShortcut("Ctrl+S")                                # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-5/qaction.html#shortcut-prop
        fileMenu.addAction(saveAction)                                  # add the save action to the file menu, documentation: https://doc.qt.io/qt-5/qwidget.html#addAction
        saveAction.triggered.connect(self.save)                         # when the menu option is selected or the shortcut is used the save slot is triggered, documenation: https://doc.qt.io/qt-5/qaction.html#triggered

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self) # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")                                # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)                                  # add this action to the file menu
        clearAction.triggered.connect(self.clear)                        # when the menu option is selected or the shortcut is used the clear slot is triggered

        #exit
        exitAction = QAction(QIcon("./icons/exit.png"), "Exit", self)
        exitAction.setShortcut("Ctrl+E")
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

        #about
        aboutAction = QAction("About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

        #help
        helpAction = QAction (QIcon("./icons/help.png"),"Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3") #TODO changed the control options to be numbers
        brushSizeMenu.addAction(threepxAction) # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction);
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction);
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        blueAction = QAction(QIcon("./icons/blue.jpg"), "Blue", self)
        blueAction.setShortcut("Ctrl+alt+B")
        brushColorMenu.addAction(blueAction)
        blueAction.triggered.connect(self.blue)

        #rubber action
        rubberAction = QAction(QIcon("./icons/rubber.png"), "Rubber", self)
        rubberAction.setShortcut("Ctrl+alt+R")
        rubberAction.triggered.connect(self.rubber)

        #brush line type
        solidlineAction= QAction(QIcon("./icons/sevenpx.png"), "Solid Line", self)
        solidlineAction.triggered.connect(self.solidline)

        dashlineAction= QAction(QIcon("./icons/dashline.jpg"), "Dash Line", self)
        dashlineAction.triggered.connect(self.dashline)

        dotlineAction=QAction(QIcon("./icons/dotline.jpg"),"Dot Line", self)
        dotlineAction.triggered.connect(self.dotline)

        dashdotlineAction=QAction(QIcon("./icons/dashdotline.png"), "Dash Dot Line", self)
        dashdotlineAction.triggered.connect(self.dashdotline)

        dashdotdotlineAction=QAction(QIcon("./icons/dashdotdotline.png"), "Dash Dot Dot Line", self)
        dashdotdotlineAction.triggered.connect(self.dashdotdotline)

        #customdashlineAction=QAction(QIcon(""), "Custom Dash Line", self)
        #customdashlineAction.triggered.connect(self.customdashline)

        #create a slider for the brush size
        self.slider=QSlider(Qt.Horizontal)
        self.slider.setMinimum(3)
        self.slider.setMaximum(25)
        self.slider.setValue(3)
        #create a status bar to give the brush size
        self.statusBar()
        #we write on the status bar what is tne size of the brush
        self.slider.setStatusTip(str(self.slider.value())+' pixels')
        #we update the size brush and the status bar
        self.slider.valueChanged[int].connect(self.changeValue)


        #create a combobox to display the brush cap type
        self.combocap = QComboBox()
        self.combocap.addItem(QIcon("./icons/roundcap.png"), "Round Cap", self)
        self.combocap.addItem(QIcon("./icons/squarecap.png"), "Square Cap", self)
        self.combocap.addItem(QIcon("./icons/flatcap.png"), "Flat Cap", self)
        self.combocap.activated.connect(self.cap)

        #create a combobox to display the brush join type
        self.combojoin = QComboBox()
        self.combojoin.addItem(QIcon("./icons/roundjoin.png"), "Round Join", self)
        self.combojoin.addItem(QIcon("./icons/beveljoin.png"), "Bevel Join", self)
        self.combojoin.addItem(QIcon("./icons/miterjoin.png"), "Miter Join", self)
        self.combojoin.activated.connect(self.join)


        #create a toolbar
        self.toolbar=self.addToolBar('')

        #add brush colors and rubber Actions
        self.toolbar.addAction(blackAction)
        self.toolbar.addAction(redAction)
        self.toolbar.addAction(greenAction)
        self.toolbar.addAction(yellowAction)
        self.toolbar.addAction(blueAction)
        self.toolbar.addAction(rubberAction)

        #add the slider for the brush size
        self.toolbar.addWidget(self.slider)

        #add brush line types Actions
        self.toolbar.addAction(solidlineAction)
        self.toolbar.addAction(dashlineAction)
        self.toolbar.addAction(dotlineAction)
        self.toolbar.addAction(dashdotlineAction)
        self.toolbar.addAction(dashdotdotlineAction)
        #self.toolbar.addAction(customdashlineAction)

        #add combobox for brush cap type
        self.toolbar.addWidget(self.combocap)

        #add combobox for brush join type
        self.toolbar.addWidget(self.combojoin)


    # event handlers
    def mousePressEvent(self, event):       # when the mouse is pressed, documentation: https://doc.qt.io/qt-5/qwidget.html#mousePressEvent
        if event.button() ==Qt.LeftButton:  # if the pressed button is the left button
            self.drawing = True             # enter drawing mode
            self.lastPoint = event.pos()    # save the location of the mouse press as the lastPoint
            print(self.lastPoint)           # print the lastPoint for debigging purposes

    def mouseMoveEvent(self, event):                        # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-5/qwidget.html#mouseMoveEvent
     if event.buttons() & Qt.LeftButton & self.drawing:     # if there was a press, and it was the left button and we are in drawing mode
            painter = QPainter(self.image)                  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-5/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, self.brushType, self.brushCap, self.brushJoin))
            painter.drawLine(self.lastPoint, event.pos())   # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint= event.pos()                     # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()                                   # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self, event):                     # when the mouse is released, documentation: https://doc.qt.io/qt-5/qwidget.html#mouseReleaseEvent
        if event.button == Qt.LeftButton:                   # if the released button is the left button, documenation: https://doc.qt.io/qt-5/qt.html#MouseButton-enum ,
            self.drawing = False                            # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(self)                      # create a new QPainter object, documenation: https://doc.qt.io/qt-5/qpainter.html
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect()) # draw the image , documentation: https://doc.qt.io/qt-5/qpainter.html#drawImage-1

    # resize event - this fuction is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image","", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath =="": # if the file path is empty
            return # do nothing and return
        self.image.save(filePath) # save file image to the file path


    def clear(self):
        self.image.fill(Qt.white)   # fill the image with white, documentaiton: https://doc.qt.io/qt-5/qimage.html#fill-2
        self.update()               # call the update method of the widget which calls the paintEvent of this class

    def exit(self):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit ?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit(app.exec_())

    def about(self):
        about= QMessageBox(self)
        about.setWindowTitle('About this Paint Application')
        about.setText('This Paint Application allows you to create files in a range of different formats ')
        about.setIcon(QMessageBox.Information)
        about.show()

    def help(self):
        help= QMessageBox(self)
        help.setWindowTitle('Help')
        help.setText('You have to select the properties of your brush (colour, size,...), then you can draw. If you want to open or save a file, clear your drawing or exit, you have to go to the file menu.')
        help.show()

    def threepx(self):              # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):                # the brush color is set to black
        self.brushColor = Qt.black

    def black(self):
        self.brushColor = Qt.black

    def red(self):
        self.brushColor = Qt.red

    def green(self):
        self.brushColor = Qt.green

    def yellow(self):
        self.brushColor = Qt.yellow

    def blue(self):
        self.brushColor=Qt.blue

    def rubber(self):
        self.brushColor=Qt.white

    #function to change the brush size thanks to the slider
    def changeValue(self, slider):
        self.brushSize=self.slider.value()
        self.slider.setStatusTip(str(self.brushSize)+' pixels')

    def solidline(self):                  #the brush line type is set to SolidLine
        self.brushType=Qt.SolidLine

    def dashline(self):
        self.brushType=Qt.DashLine

    def dotline(self):
        self.brushType=Qt.DotLine

    def dashdotline(self):
        self.brushType=Qt.DashDotLine

    def dashdotdotline(self):
        self.brushType=Qt.DashDotDotLine

    #def customdashline(self):
    #   self.brushType=Qt.CustomDashLine

    #function for the combocap
    def cap(self):
        cap = self.combocap.currentText()
        if cap == "Round Cap":
            self.brushCap=Qt.RoundCap
        if cap == "Square Cap":
            self.brushCap=Qt.SquareCap
        if cap == "Flat Cap":
            self.brushCap=Qt.FlatCap

    #function for the combojoin
    def join(self):
        join=self.combojoin.currentText()
        if join == "Round Join":
            self.brushJoin=Qt.RoundJoin
        if join == "Bevel Join":
            self.brushJoin=Qt.BevelJoin
        if join == "Miter Join":
            self.brushJoin=Qt.MiterJoin


    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file doalog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":   # if not file is selected exit
            return
        with open(filePath, 'rb') as f: #open the file in binary mode for reading
            content = f.read() # read the file
        self.image.loadFromData(content) # load the data into the file
        width = self.width() # get the width of the current QImage in your application
        height = self.height() # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height) # scale the image from file and put it in your QImage
        self.update() # call the update method of the widget which calls the paintEvent of this class


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = PaintingApplication()
    window.show()
    app.exec() # start the event loop running