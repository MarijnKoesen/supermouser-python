# pip install pyuserinput pyqt5
import sys
from pymouse import PyMouse
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CustomWindow(QMainWindow):
    def __init__(self, pymouse): 
        super().__init__(); 
        self.__resetWorkingArea()
        self.mouse = pymouse

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.5)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))   

        drawWorkingArea = False
        if drawWorkingArea:
            painter.fillRect(
                self.workingArea[0],
                self.workingArea[1], 
                self.workingArea[2],
                self.workingArea[3], 
		Qt.white
	    )
        else:
            painter.fillRect(
                0,
                0, 
                self.currentScreenSize.width(),
                self.workingArea[1],
		Qt.white
	    )
            painter.fillRect(
                0,
                self.workingArea[1], 
                self.workingArea[0],
                self.currentScreenSize.height(),
		Qt.white
	    )
            painter.fillRect(
                self.workingArea[0] + self.workingArea[2],
                self.workingArea[1], 
                self.currentScreenSize.width(),
                self.workingArea[3], 
		Qt.white
	    )
            painter.fillRect(
                self.workingArea[0],
                self.workingArea[1] + self.workingArea[3], 
                self.currentScreenSize.width(),
                self.currentScreenSize.height(),
		Qt.white
	    )

    def __resetWorkingArea(self):
        self.currentScreenSize = QDesktopWidget().screenGeometry(-1)
        self.workingArea = [0, 0, self.currentScreenSize.width(), self.currentScreenSize.height()]

    def __updateWorkingArea(self, newWorkingArea):
        self.workingArea = newWorkingArea
        self.mouse.move(
            self.workingArea[0] + (self.workingArea[2] / 2),
            self.workingArea[1] + (self.workingArea[3] / 2),
        )
        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_H:
            self.__updateWorkingArea([
		self.workingArea[0], 
                self.workingArea[1],
                self.workingArea[2] / 2, 
                self.workingArea[3]
            ])
            return

        if e.key() == Qt.Key_J:
            self.__updateWorkingArea([
		self.workingArea[0], 
                self.workingArea[1] + (self.workingArea[3] / 2),
                self.workingArea[2], 
                self.workingArea[3] / 2
            ])
            return

        if e.key() == Qt.Key_K:
            self.__updateWorkingArea([
		self.workingArea[0], 
                self.workingArea[1], 
                self.workingArea[2], 
                self.workingArea[3] / 2
            ])
            return

        if e.key() == Qt.Key_L:
            self.__updateWorkingArea([
		self.workingArea[0] + (self.workingArea[2] / 2),
                self.workingArea[1], 
                self.workingArea[2] / 2, 
                self.workingArea[3]
            ])
            return

        if e.key() == Qt.Key_F:
            self.mouse.click(
                self.mouse.position()[0],
                self.mouse.position()[1],
                1 # left click
            )
            return

        if e.key() == Qt.Key_G:
            self.mouse.click(
                self.mouse.position()[0],
                self.mouse.position()[1],
                2 # right click
            )
            return

        if e.key() == Qt.Key_Q:
            self.close()


app = QApplication(sys.argv)

# Create the main window
mouse = PyMouse()
window = CustomWindow(mouse)

window.setWindowFlags(
    Qt.FramelessWindowHint 
    | Qt.WindowStaysOnTopHint 
    #| Qt.NoDropShadowWindowHint
)
window.setAttribute(Qt.WA_NoSystemBackground, True)
window.setAttribute(Qt.WA_TranslucentBackground, True)

# Run the application
window.showMaximized()
sys.exit(app.exec_())
