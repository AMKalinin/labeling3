from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QProgressBar)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
#import segflex_seg_window as seg_window
import utils
import re
import h5py
import cv2

class project_widget_new(QGroupBox):
    def __init__(self, path, parent, main):
        super().__init__(parent=parent)
        self.main = main
        self.path = path
        self.init_ui()

    def init_ui(self):
        self.set_layouts()
        self.adjust_size()
        self.init_content()
        self.fill_layouts()
        self.connect_ui()

    def set_layouts(self):
        self.layout = QHBoxLayout()
        self.layout_preview = QVBoxLayout()
        self.layout_info = QVBoxLayout()
        self.layout_actions = QVBoxLayout()

        self.layout.addLayout(self.layout_preview)
        self.layout.addLayout(self.layout_info)
        self.layout.addLayout(self.layout_actions)

        self.setLayout(self.layout)

    def adjust_size(self):
        self.setMaximumHeight(130)

    def init_content(self):
        self.init_info()
        self.init_progressbar()
        self.open = QPushButton("Открыть проект")

    def init_info(self):
        self.name = utils.get_name(self.path)
        self.description = utils.get_description(self.path)
        self.alltasks = utils.get_alltasks(self.path)
        self.donetasks = utils.get_donetasks(self.path)
        self.startdate = time.ctime(utils.get_startdate(self.path))
        self.lastupdate = time.ctime(utils.get_lastupdate(self.path))
        self.info = QLabel(self.name + '\n' 
                        + self.description + '\n'
                        + str(self.donetasks) + ' / ' + str(self.alltasks) + '\n'
                        + self.startdate + ' / ' + self.lastupdate)

    def init_progressbar(self):
        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(self.alltasks)
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(self.donetasks)

    def fill_layouts(self):
        self.layout_actions.addWidget(self.open)
        self.layout_info.addWidget(self.info)
        self.layout_info.addWidget(self.progressbar)
    
    def connect_ui(self):
        self.open.clicked.connect(self.on_open)

    def on_open(self):
        self.main.signal_openproject.emit(self.path)
