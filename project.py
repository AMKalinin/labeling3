from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF, QRect
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QProgressBar)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import utils
import re
import h5py
import cv2

class qsslabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()

class projectWidget(QGroupBox):
    def __init__(self, path, parent, main):
        super().__init__(parent=parent)
        self.main = main
        self.path = path
        self.init_ui()
        self.setMouseTracking(True)

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
        self.init_preview()
        self.init_info()
        self.init_progressbar()
        self.open = QPushButton("Открыть")
        self.open.setObjectName('button_primary')
        self.delete = QPushButton("Удалить")
        self.delete.setObjectName('button_danger')

    def init_info(self):
        self.name = utils.get_name(self.path)
        self.setTitle('Имя: ' + self.name)
        self.description = utils.get_description(self.path)
        self.description = utils.cut_long_string(self.description, 30)
        self.alltasks = utils.get_alltasks(self.path)
        self.donetasks = utils.get_donetasks(self.path)
        #self.startdate = time.ctime(utils.get_startdate(self.path))
        self.lastupdate = time.ctime(utils.get_lastupdate(self.path))
        #self.info = qsslabel(self.name + '\n' 
        #                + self.description + '\n'
        #                + str(self.donetasks) + ' / ' + str(self.alltasks) + '\n'
        #                + self.startdate + ' / ' + self.lastupdate)
        self.info = qsslabel()
        self.info.setText(#self.name + '\n'
                        'Описание: ' + self.description + '\n'
                        + 'Выполнено задач: ' + str(self.donetasks) + ' / ' + str(self.alltasks) + '\n'
                        + 'Последнее изменение: '  + self.lastupdate)
    
    def init_preview(self):
        self.preview = qsslabel(self)
        pixmap = QPixmap(100, 100)
        painter = QPainter(pixmap)
        topLeftY = 0
        width = 25
        height = 25
        index = 0
        for row in range(4):
            topLeftX = 0
            for collumn in range(4):
                target = QRectF(QRect(topLeftX, topLeftY, width, height))
                image = utils.create_microimage(self.path, index)
                painter.drawImage(target, image, QRectF(image.rect()))
                topLeftX += width
                index += 1
            topLeftY += height
        painter.end()# = None #correct destroy?
        self.preview.setPixmap(pixmap)

    def init_progressbar(self):
        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(self.alltasks)
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(self.donetasks)

    def fill_layouts(self):
        self.layout_actions.addWidget(self.open)
        #self.layout_actions.addWidget(self.delete)
        self.layout_info.addWidget(self.info)
        self.layout_info.addWidget(self.progressbar)
        self.layout_preview.addWidget(self.preview)
    
    def connect_ui(self):
        self.open.clicked.connect(self.on_open)

    def on_open(self):
        self.main._open_project.emit(self.path)

    def enterEvent(self, event):
        with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/style/project_hover.qss", 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)

    
    def leaveEvent(self, event):
        with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/style/project_unhover.qss", 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)

