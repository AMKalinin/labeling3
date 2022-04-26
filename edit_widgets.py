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
import segflex_seg_window as seg
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
        self.layout.addWidget(self.btn_showall, 0, 1)
        self.layout.addWidget(self.btn_hideall, 0, 2)
        self.layout.addWidget(self.combo, 0, 3)


    def init_widgets(self):
        self.edit = view_widgets.view_edit(parent=None, file_link=self.hdf, current_task=self.index)
        self.btn_showall = QPushButton("showall")
        self.btn_hideall = QPushButton("hideall")

        self.combo = QComboBox()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.task_attrs.COUNT.value and name != classifier.task_attrs.STATUS.value:
                self.combo.addItem(value)

    def connect_ui(self):
        self.btn_showall.clicked.connect(self.edit.show)
        self.btn_hideall.clicked.connect(self.edit.hide)

