#!/usr/bin/env python3
# pip install pyqt5 psutil pynput
# on linux also: sudo apt-get install  python-xlib
import os
import psutil
import sys
import time
from pynput.mouse import Button, Controller
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

def current_screen_size(mouse_position):
    for screen in app.screens():
        (x, y) = mouse_position
        screen_geom = screen.availableGeometry();
        if (x >= screen_geom.left() and y >= screen_geom.top() and
            x <= screen_geom.left() + screen_geom.width() and
            y <= screen_geom.top() + screen_geom.height()):
           return screen_geom
    return app.desktop().availableGeometry(-1)


class CustomWindow(QMainWindow):
    def __init__(self, mouse): 
        super().__init__()
        self.mouse = mouse
        self.currentScreenSize = current_screen_size(self.mouse.position)
        self.reset()

    def reset(self):
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
        painter.setBrush(Qt.blue)
        painter.setPen(QPen(Qt.blue))

        painter.fillRect(self.leftRect, Qt.blue)
        painter.fillRect(self.rightRect, Qt.blue)
        painter.fillRect(self.topRect, Qt.blue)
        painter.fillRect(self.bottomRect, Qt.blue)

    def keyPressEvent(self, e):
        width = self.currentScreenSize.width()
        height = self.currentScreenSize.height()
        offset_x = self.currentScreenSize.left()
        offset_y = self.currentScreenSize.top()

        # calculate x & y as if top-left of current screen is (0, 0)
        x, y = self.mouse.position
        x -= offset_x
        y -= offset_y

        x = int(x)
        y = int(y)

        # however when using x & y, translate them back..
        def mouse_move(x, y):
            self.mouse.position = (offset_x + x, offset_y + y)

        def mouse_click(x, y, button):
            self.mouse.press(Button.left)
            self.mouse.release(Button.left)

        if e.key() == Qt.Key_H:
            self.rightExcluded = width - x
            self.rightRect = QRect(x, 0, width, height)
            mouse_move(int(x - ((x - self.leftExcluded) / 2)), y)
            self.repaint()
            return

        if e.key() == Qt.Key_L:
            self.leftExcluded = x
            self.leftRect = QRect(0, 0, x, height)
            mouse_move(int(x + ((width - x - self.rightExcluded) / 2)), y)
            self.repaint()
            return

        if e.key() == Qt.Key_J:
            self.topExcluded = y
            self.topRect = QRect(0, 0, width, y)
            mouse_move(x, int(y + ((height - y - self.bottomExcluded) / 2)))
            self.repaint()
            return

        if e.key() == Qt.Key_K:
            self.bottomExcluded = height - y
            self.bottomRect = QRect(0, y, width, height)
            mouse_move(x, int(y - ((y - self.topExcluded) / 2)))
            self.repaint()
            return

        if e.key() == Qt.Key_F:
            self.close()
            QApplication.processEvents()

            time.sleep(0.1)
            mouse_click(x, y, 1)  # left click
            kill_proc_tree(os.getpid())
            return

        if e.key() == Qt.Key_D:
            self.close()
            QApplication.processEvents()

            time.sleep(0.1)
            mouse_click(x, y, 1)  # left click
            time.sleep(0.1)
            mouse_click(x, y, 1)  # left click
            kill_proc_tree(os.getpid())
            return

        if e.key() == Qt.Key_G:
            self.close()
            QApplication.processEvents()

            time.sleep(0.1)
            mouse_click(x, y, 2)  # right click
            kill_proc_tree(os.getpid())
            return

        if e.key() == Qt.Key_M:
            self.reset()
            self.repaint()
            return

        if e.key() == Qt.Key_Q or e.key() == Qt.Key_Escape:
            self.close()
            kill_proc_tree(os.getpid())


app = QApplication(sys.argv)

# Create the main window
mouse = Controller()
window = CustomWindow(mouse)

window.setWindowFlags(
    Qt.FramelessWindowHint
    | Qt.WindowStaysOnTopHint
    | Qt.X11BypassWindowManagerHint
   |  Qt.ActiveWindowFocusReason
    | Qt.Tool
    | Qt.ToolTip
    | Qt.WindowTransparentForInput
    | Qt.WindowActive
 #   | Qt.WindowSystemMenuHint
 #   | Qt.WindowTitleHint
 #   | Qt.Widget
 #   | Qt.NoDropShadowWindowHint
#    | Qt.Popup
#    | Qt.SplashScreen
#    | Qt.Drawer
#    | Qt.Sheet
#    | Qt.Dialog
)
#window.setParent(0);# // Create TopLevel-Widget
#setAttribute(Qt::WA_NoSystemBackground, true);
#setAttribute(Qt::WA_TranslucentBackground, true);  
#setAttribute(Qt::WA_PaintOnScreen); // not needed in Qt 5.2 and up
window.setAttribute(Qt.WA_NoSystemBackground, True)
window.setAttribute(Qt.WA_TranslucentBackground, True)
if False:
    window.setAttribute(Qt.WA_PaintOnScreen, True)
    window.setStyleSheet("background:transparent;")

if platform == "linux" or platform == "linux2":
    pass # window.setAttribute(Qt.WA_X11NetWmWindowTypeSplash, True)
elif platform == "darwin":
    pass
elif platform == "win32":
    pass

# Run the application
#window.showFullScreen()  # on my X11 window manager this prevents all other windows from being drawn
#window.showMaximized()   # .. and this also didn't do anything..
dimensions = current_screen_size(mouse.position)
#print(dimensions)

window.setWindowFlags(
    Qt.FramelessWindowHint
    #| Qt.WindowStaysOnTopHint
    #| Qt.NoDropShadowWindowHint
)

window.setAttribute(Qt.WA_NoSystemBackground, True)
window.setAttribute(Qt.WA_TranslucentBackground, True)
#window.setAttribute(Qt.WA_TransparentForMouseEvents, True)

window.move(dimensions.left(), dimensions.top())
window.resize(dimensions.width(), dimensions.height())
window.showNormal()
window.raise_()
window.activateWindow()

sys.exit(app.exec_())
