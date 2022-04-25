from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene)
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


class project_description_new(QGroupBox):
    def __init__(self, project_file=None, signal=None, project_path=None):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.init_content()
        self.init_menu()
        self.adjust_window()

    def init_content(self):
        self.name = ' проект не открыт'
        self.classes = ' проект не открыт'
        self.time_c = ' проект не открыт'
        self.time_u = ' проект не открыт'
        self.description = ' проект не открыт'
        self.task_count = ' проект не открыт'

        self.btn_addtask = QPushButton("Добавить задачу")
        self.btn_edittask = QPushButton("edit task")

    def init_menu(self):
        self.menu = QListWidget()

        self.name = QListWidgetItem(classifier.HDF_FILE_NAME + self.name)
        self.classes = QListWidgetItem(classifier.HDF_FILE_CLASSES + self.classes)
        self.time_c = QListWidgetItem(classifier.HDF_FILE_TIME_C + self.time_c)
        self.time_u = QListWidgetItem(classifier.HDF_FILE_TIME_U + self.time_u)
        self.description = QListWidgetItem(classifier.HDF_FILE_DESCRIPTION + self.description)
        self.task_count = QListWidgetItem(classifier.HDF_FILE_TASK_COUNT + self.task_count)

        self.menu.addItem(self.name)
        self.menu.addItem(self.classes)
        self.menu.addItem(self.time_c)
        self.menu.addItem(self.time_u)
        self.menu.addItem(self.description)
        self.menu.addItem(self.task_count)

    def adjust_window(self):
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.btn_addtask)
        self.layout.addWidget(self.btn_edittask)

        self.setLayout(self.layout)

    def parse_description(self, hdf):
        self.name.setText(classifier.HDF_FILE_NAME + hdf.attrs[classifier.HDF_FILE_NAME])
        self.description.setText(classifier.HDF_FILE_DESCRIPTION + hdf.attrs[classifier.HDF_FILE_DESCRIPTION])
        self.task_count.setText(classifier.HDF_FILE_TASK_COUNT +  str(hdf.attrs[classifier.HDF_FILE_TASK_COUNT])) #str?
        """
        self.file_name = hdf.attrs[classifier.HDF_FILE_NAME]
        self.file_classes = hdf.attrs[classifier.HDF_FILE_CLASSES]
        self.file_time_c = hdf.attrs[classifier.HDF_FILE_TIME_C]
        self.file_time_u = hdf.attrs[classifier.HDF_FILE_TIME_U]
        self.file_description = hdf.attrs[classifier.HDF_FILE_DESCRIPTION]
        self.file_task_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
        """

        """
        self.item_name.setText(classifier.HDF_FILE_NAME + self.file_name)
        #self.item_classes.setText(classifier.HDF_FILE_CLASSES + self.file_classes)
        #self.item_time_u.setText(classifier.HDF_FILE_TIME_U + self.file_time_u)
        self.item_description.setText(classifier.HDF_FILE_DESCRIPTION + self.file_description)
        self.item_task_count.setText(classifier.HDF_FILE_TASK_COUNT + str(int(self.file_task_count)))
        """

class higher_control(QGroupBox):
    def __init__(self, signal, parent=None):
        super().__init__()
        self.signal = signal
        self.init_ui()

    def init_ui(self):
        self.init_content()
        self.set_layouts()
        self.fill_layouts()
        self.connect_ui()

    def set_layouts(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def fill_layouts(self):
        self.layout.addWidget(self.btn_new)
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_based)

    def init_content(self):
        self.btn_new = QPushButton("Создать новый файл проекта")
        self.btn_add = QPushButton("Добавить проект из ...")
        self.btn_based = QPushButton("Создать проект на основе существующего")

    def connect_ui(self):
        self.btn_new.clicked.connect(self.on_new)

    def on_new(self):
        self.dialog = new_project.new_project_dialog_new(signal=self.signal)
        self.dialog.exec_()


class view_control(QGroupBox):
    def __init__(self, signal_showall, signal_edittask):
        super().__init__()
        self.signal_showall = signal_showall
        self.signal_edittask = signal_edittask
        self.create_pallete()
        self.init_ui()

    def init_ui(self):
        self.btn_previous = QPushButton("<<")
        self.btn_next = QPushButton(">>")
        self.btn_showall = QPushButton("show all")
        self.btn_showall.clicked.connect(self.on_showall)
        self.btn_hideall = QPushButton("hide all")
        self.btn_hideall.clicked.connect(self.on_hideall)
        self.btn_edittask = QPushButton("edit task")
        self.btn_edittask.clicked.connect(self.on_edittask)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_previous)
        self.layout.addWidget(self.btn_next)
        self.layout.addWidget(self.btn_showall)
        self.layout.addWidget(self.btn_hideall)
        self.layout.addWidget(self.btn_edittask)
        self.layout.addWidget(self.list)

        self.setLayout(self.layout)
    
    def on_showall(self):
        self.signal_showall.emit(1)

    def on_hideall(self):
        self.signal_showall.emit(-1)

    def on_edittask(self):
        self.signal_edittask.emit(-1)

    def create_pallete(self):
        color_index = 2
        self.list = QListWidget()
        for cclass in classifier.classes:
            pixmap = QPixmap(50,50)
            color = QColor(Qt.GlobalColor(color_index))
            pixmap.fill(color)
            self.list.addItem(QListWidgetItem(QIcon(pixmap), cclass.value))
            color_index += 1
            if color_index == 19:
                color_index = 2

    def adjust_pallete(self, hdf):
        color_index = 2
        self.layout.removeWidget(self.list)
        self.list.deleteLater()
        self.list = QListWidget()
        for cclass in hdf.attrs[classifier.HDF_FILE_CLASSES]:
            pixmap = QPixmap(50,50)
            color = QColor(Qt.GlobalColor(color_index))
            pixmap.fill(color)
            self.list.addItem(QListWidgetItem(QIcon(pixmap), cclass))
            color_index += 1
            if color_index == 19:
                color_index = 2

        self.layout.addWidget(self.list)