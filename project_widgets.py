from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import segflex_seg_window as seg_window
import re
import h5py
import classifier
import cv2

class project_widget_new(QGroupBox):
    def __init__(self, signal, path, parent=None):
        super().__init__()
        self.signal = signal
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
        self.setMaximumHeight(120)

    def init_content(self):
        self.btn_open = QPushButton("Открыть проект")
        self.info = QLabel(self.path)

    def fill_layouts(self):
        self.layout_actions.addWidget(self.btn_open)
        self.layout_info.addWidget(self.info)
    
    def connect_ui(self):
        self.btn_open.clicked.connect(self.on_open)

    def on_open(self):
        self.signal.emit(self.path)