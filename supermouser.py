#!/usr/bin/env python3
# pip install pyuserinput pyqt5
# on linux also: sudo apt-get install  python-xlib
import os
import psutil
import sys
from pymouse import PyMouse
from sys import platform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def kill_proc_tree(pid, including_parent=True):
    """
    Perhaps only needed in Linux, no matter what the proces just wouldn't exit.
    Even after manually controlling the event loop, for now this is a workaround.
    """
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()


class CustomWindow(QMainWindow):
    def __init__(self, pymouse): 
        super().__init__()
        self.mouse = pymouse
        self.currentScreenSize = app.desktop().availableGeometry()
        # number of pixels "excluded" using divide & conquer
        self.leftExcluded = 0
        self.rightExcluded = 0
        self.topExcluded = 0
        self.bottomExcluded = 0
        # corresponding rectangles to visualize excluded areas
        self.leftRect = QRect(0, 0, 0, 0)
        self.rightRect = QRect(0, 0, 0, 0)
        self.topRect = QRect(0, 0, 0, 0)
        self.bottomRect = QRect(0, 0, 0, 0)

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.5)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))   

        painter.fillRect(self.leftRect, Qt.white)
        painter.fillRect(self.rightRect, Qt.white)
        painter.fillRect(self.topRect, Qt.white)
        painter.fillRect(self.bottomRect, Qt.white)

    def keyPressEvent(self, e):
        x, y = self.mouse.position()
        width = self.currentScreenSize.width()
        height = self.currentScreenSize.height()

        if e.key() == Qt.Key_H:
            self.rightExcluded = width - x
            self.rightRect = QRect(x, 0, width, height)
            self.repaint()
            self.mouse.move(int(x - ((x - self.leftExcluded) / 2)), y)
            return

        if e.key() == Qt.Key_L:
            self.leftExcluded = x
            self.leftRect = QRect(0, 0, x, height)
            self.repaint()
            self.mouse.move(int(x + ((width - x - self.rightExcluded) / 2)), y)
            return

        if e.key() == Qt.Key_J:
            self.topExcluded = y
            self.topRect = QRect(0, 0, width, y)
            self.repaint()
            self.mouse.move(x, int(y + ((height - y - self.bottomExcluded) / 2)))
            return

        if e.key() == Qt.Key_K:
            self.bottomExcluded = height - y
            self.bottomRect = QRect(0, y, width, height)
            self.repaint()
            self.mouse.move(x, int(y - ((y - self.topExcluded) / 2)))
            return

        if e.key() == Qt.Key_F:
            self.close()
            self.mouse.click(x, y, 1)  # left click
            kill_proc_tree(os.getpid())
            return

        if e.key() == Qt.Key_D:
            self.close()
            self.mouse.click(x, y, 1)  # left click
            self.mouse.click(x, y, 1)  # left click
            kill_proc_tree(os.getpid())
            return

        if e.key() == Qt.Key_G:
            self.close()
            self.mouse.click(x, y, 2)  # right click
            kill_proc_tree(os.getpid())
            return

        if e.key() == Qt.Key_Q:
            self.close()
            kill_proc_tree(os.getpid())


app = QApplication(sys.argv)

# Create the main window
mouse = PyMouse()
window = CustomWindow(mouse)

window.setWindowFlags(
    Qt.FramelessWindowHint
    | Qt.WindowStaysOnTopHint
    #| Qt.WindowSystemMenuHint
    #| Qt.WindowTitleHint
    #| Qt.NoDropShadowWindowHint
    #| Qt.Tool
)

window.setAttribute(Qt.WA_NoSystemBackground, True)
window.setAttribute(Qt.WA_TranslucentBackground, True)

if platform == "linux" or platform == "linux2":
    window.setAttribute(Qt.WA_X11NetWmWindowTypeSplash, True)
elif platform == "darwin":
    pass
elif platform == "win32":
    pass

# Run the application
# window.showFullScreen()  # on my X11 window manager this prevents all other windows from being drawn
# window.showMaximized()   # .. and this also didn't do anything..
dimensions = app.desktop().availableGeometry()
window.move(0, 0)
window.resize(dimensions.width(), dimensions.height())
window.showNormal()
sys.exit(app.exec_())
