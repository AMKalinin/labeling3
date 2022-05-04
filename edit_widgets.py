from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene, QMenuBar)
from PyQt5 import QtWidgets, QtGui, QtCore

import new_project
import project_widgets
import task_widgets
#import segflex_seg_window as seg
import view_widgets
import os
import json
import classifier
import utils
import h5py
import time
import re
import cv2
import control_widgets
import tab_widget


class edit_widget(QDialog):
    def __init__(self, index, hdf):
        super().__init__()
        self.index = index
        self.hdf = hdf
        
        self.init_widgets()
        self.init_layout()
        self.connect_ui()

    def init_layout(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
    
        self.layout.addWidget(self.edit, 0, 0)
        self.layout.addWidget(self.showall, 0, 1)
        self.layout.addWidget(self.hideall, 0, 2)
        #self.layout.addWidget(self.combo, 0, 3)
        self.layout.addWidget(self.polygon, 0, 4)
        self.layout.addWidget(self.none, 0, 5)
        self.layout.addWidget(self.p_list, 0, 6)
        self.layout.addWidget(self.save, 0, 7)

    def init_widgets(self):
        self.edit = view_widgets.view_edit(parent=None, file_link=self.hdf, current_task=self.index)
        self.showall = QPushButton("showall")
        self.hideall = QPushButton("hideall")
        self.polygon = QPushButton("new polygon")
        self.none = QPushButton("none")
        self.polygon_list()
        self.save = QPushButton("save")
        #self.list = QListWidget()

        """
        self.combo = QComboBox()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.combo.addItem(value)
        """
    def connect_ui(self):
        self.showall.clicked.connect(self.edit.show)
        self.hideall.clicked.connect(self.edit.hide)
        self.polygon.clicked.connect(self.edit.add_polygon)
        self.none.clicked.connect(self.edit.add_none)
        self.save.clicked.connect(self.edit.save_shape)

    def polygon_list(self):
        self.p_list = QListWidget()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.p_list.addItem(value)

