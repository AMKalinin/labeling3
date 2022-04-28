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
import edit_widgets

class main_window(QMainWindow):
    signal_parseprojects = pyqtSignal()
    signal_openproject = pyqtSignal(str)
    signal_showall = pyqtSignal(int)
    signal_edittask = pyqtSignal(int)
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        self.file = None
        self.init_ui()
        
    def init_ui(self):
        self.adjust_window()
        self.init_widgets()
        self.place_blocks()
        self.connect_ui()

    def adjust_window(self):
        self.main_frame = QFrame()
        self.setCentralWidget(self.main_frame)
        self.setWindowTitle("Segmentation app. 0.9")
        self.resize(1024, 600)
        self.main_layout = QGridLayout()
        self.main_frame.setLayout(self.main_layout)


    def init_widgets(self):
        self.tab_new = tab_widget.my_tab(signal=self.signal_openproject, signal2=self.signal_showall, signal_edittask=self.signal_edittask)
        self.higher_control = control_widgets.higher_control(signal=self.signal_parseprojects)
        self.description = control_widgets.project_description_new()
        self.navigation = control_widgets.view_control(self.signal_showall, self.signal_edittask)

    def place_blocks(self):
        self.main_layout.addWidget(self.tab_new, 0, 0, 4, 1)
        self.main_layout.addWidget(self.higher_control, 0, 1)
        self.main_layout.addWidget(self.description, 0, 1)
        self.main_layout.addWidget(self.navigation, 0, 1)
        self.show_higher_control()

    def connect_ui(self):
        self.signal_parseprojects.connect(self.tab_new.parse_projects)
        self.signal_openproject.connect(self.open_project_routine)
        self.tab_new.currentChanged.connect(self.show_tab_new)
        self.description.btn_addtask.clicked.connect(self.add_task)
        #self.description.btn_edittask.clicked.connect(self.on_edittask)
        self.navigation.btn_previous.clicked.connect(self.previous_view)
        self.navigation.btn_next.clicked.connect(self.next_view)
        #self.navigation.btn_edittask.clicked.connect(self.on_edittask)
        self.signal_edittask.connect(self.on_edittask)
    
    def show_tab(self):
        if self.tab.currentWidget() == self.tab_split:
            self.show_description()
        elif self.tab.currentWidget() == self.tab_projects_area:
            self.show_higher_control()
        elif self.tab.currentWidget() == self.tab_view:
            self.show_navigation()
    
    def show_tab_new(self):
        if self.tab_new.currentWidget() == self.tab_new.split:
            self.show_description()
        elif self.tab_new.currentWidget() == self.tab_new.projects:
            self.show_higher_control()
        elif self.tab_new.currentWidget() == self.tab_new.view:
            self.show_navigation()

    def show_description(self):
        self.higher_control.setVisible(False)
        self.navigation.setVisible(False)
        self.description.setVisible(True)

    def show_higher_control(self):
        self.higher_control.setVisible(True)
        self.navigation.setVisible(False)
        self.description.setVisible(False)

    def show_navigation(self):
        self.higher_control.setVisible(False)
        self.description.setVisible(False)
        self.navigation.setVisible(True)

    @pyqtSlot(str)
    def open_project_routine(self, project_path):
        if self.file:
            self.file.close()
        self.file = h5py.File(project_path, 'r+')
        self.tab_new.parse_tasks(self.file)
        self.description.parse_description(self.file)
        self.tab_new.parse_view(self.file)
        self.navigation.adjust_pallete(self.file)

    def adjust_opened_project(self):
        self.tab_new.parse_tasks(self.file)
        self.description.parse_description(self.file)
        self.tab_new.parse_view(self.file)

    def add_task(self):
        #print(classifier.task_attrs.TO_DO.value)
        #"""
        if self.file:
            hdf = self.file
            task = QFileDialog.getOpenFileName()[0]
            if task:
                tasks_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
                task_numpy = cv2.imread(task)
                hdf.create_dataset(str(tasks_count), data=task_numpy)
                hdf[str(tasks_count)].attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_0
                hdf[str(tasks_count)].attrs[classifier.HDF_TASK_POLYGON_COUNT] = 0
                #hdf[str(tasks_count)].attrs[classifier.task_attrs.STATUS.value] = classifier.task_attrs.TO_DO.value
                #hdf[str(tasks_count)].attrs[classifier.task_attrs.COUNT.value] = 0
                hdf.attrs[classifier.HDF_FILE_TASK_COUNT] += 1
                self.adjust_opened_project()
        #"""

    @pyqtSlot(int)
    def on_edittask(self, index=-1):
        current_task = self.tab_new.view_w.current_task()
        if index != -1:
            current_task = index
        self.edit = edit_widgets.edit_widget(current_task, self.file)
        self.edit.exec_()


    def on_showall(self):
        print("showall")
        self.signal_showall.emit(1)

    def previous_view(self):
        self.tab_new.change_view(index=-1)

    def next_view(self):
        self.tab_new.change_view(index=+1)
