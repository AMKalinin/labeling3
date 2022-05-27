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
    signal_parsepolygons = pyqtSignal()
    def __init__(self, main, index, hdf):
        super().__init__()
        self.main = main
        self.index = index
        self.hdf = hdf
        
        self.init_widgets()
        self.init_layout()
        self.connect_ui()
        #self.polygon_list()

    def init_layout(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
    
        self.layout.addWidget(self.edit, 0, 0)
        #self.layout.addWidget(self.showall, 0, 1)
        #self.layout.addWidget(self.hideall, 0, 2)
        #self.layout.addWidget(self.combo, 0, 3)

        self.layout.addWidget(self.polygon, 0, 4)
        #self.layout.addWidget(self.new_item, 1, 4)
        #self.layout.addWidget(self.discard_shape, 2, 4)

        #self.layout.addWidget(self.none, 0, 5)
        self.layout.addWidget(self.edit.attr_list, 0, 6)

        self.layout.addWidget(self.save, 0, 7)
        self.layout.addWidget(self.delete, 2, 7)
        #self.layout.addWidget(self.edit_points, 1, 7)
        #self.layout.addWidget(self.edit_class, 3, 7)

        self.layout.addWidget(self.edit.pallete, 0, 9)


        

    def init_widgets(self):
        self.edit = view_widgets.view_edit(parent=None, main=self.main, current_task=self.index)
        #self.showall = QPushButton("showall")
        #self.hideall = QPushButton("hideall")
        self.polygon = QPushButton("new polygon")
        self.new_item = QPushButton("new item")
        self.discard_shape = QPushButton("discard_shape")
        self.none = QPushButton("none")
        #self.attr_list = QListWidget()
        self.save = QPushButton("save")
        self.delete = QPushButton("delete")
        #self.list = QListWidget()
        self.edit_points = QPushButton("edit points")
        self.edit_class = QPushButton("edit class")

        """
        self.combo = QComboBox()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.combo.addItem(value)
        """
    def connect_ui(self):
        #self.showall.clicked.connect(self.edit.show)
        #self.hideall.clicked.connect(self.edit.hide)
        self.polygon.clicked.connect(self.edit.add_polygon)
        self.none.clicked.connect(self.edit.add_none)
        self.save.clicked.connect(self.edit.save_attrhdf)
        #self.signal_parsepolygons.connect(self.polygon_list)
        self.delete.clicked.connect(self.edit.delete_attrlistitem)
        self.edit_points.clicked.connect(self.edit.edit_attr)

    """
    def polygon_list(self):
        #print("parsed")
        #if self.attr_list:
        #    self.attr_list.deleteLater()
        self.attr_list.clear()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.attr_list.addItem(value)
    """

