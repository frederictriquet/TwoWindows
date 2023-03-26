from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt6 import QtGui

import sys
import vlc

from random import randint

class Singleton:
    __instance = None

    def __new__(cls,*args, **kwargs):
        if cls.__instance is None :
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance


class Data(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.mediaplayer = vlc.MediaPlayer()
        self.media = None
    
    def play_video(self, filename) -> None:
        data.media = vlc.Media(filename)
        data.mediaplayer.set_media(data.media)
        data.mediaplayer.play()



class SlaveWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        # self.label = QLabel("Another Window % d" % randint(0,100))
        # layout.addWidget(self.label)
        # In this widget, the video will be drawn
        # if sys.platform == "darwin": # for MacOS
        #     from PyQt6.QtWidgets import QMacCocoaViewContainer	
        #     self.videoframe = QMacCocoaViewContainer(0)
        # else:
        self.videoframe = QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.ColorRole.Window, QtGui.QColor(255,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.videoframe = QFrame(frameShape=QFrame.Shape.Box, frameShadow=QFrame.Shadow.Raised)
        layout.addWidget(self.videoframe)
        self.setLayout(layout)

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            data.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            data.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            data.mediaplayer.set_nsobject(int(self.videoframe.winId()))



class MasterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.button_show = QPushButton("Show Window")
        self.button_show.clicked.connect(lambda x: slave_window.show())
        self.main_layout.addWidget(self.button_show)
        self.button_play1 = QPushButton("Play 1")
        self.button_play1.clicked.connect(lambda x: data.play_video("./Videos/a.mp4"))
        self.main_layout.addWidget(self.button_play1)
        self.button_play2 = QPushButton("Play 2")
        self.button_play2.clicked.connect(lambda x: data.play_video("./Videos/b.mp4"))
        self.main_layout.addWidget(self.button_play2)
        self.button_quit = QPushButton("Quit")
        self.button_quit.clicked.connect(sys.exit)
        self.main_layout.addWidget(self.button_quit)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.main_layout)


app = QApplication(sys.argv)
data = Data()
master_window = MasterWindow()
master_window.show()
slave_window = SlaveWindow()
# slave_window.show()
slave_window.resize(800,600)

app.exec()