from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QSize
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
import edit_widgets

class main_window(QMainWindow):
    signal_parseprojects = pyqtSignal()
    signal_openproject = pyqtSignal(str)
    signal_showall = pyqtSignal(int)
    signal_edittask = pyqtSignal(int)
    signal_editdescription = pyqtSignal(str)
    def __init__(self):
        QMainWindow.__init__(self, flags=QtCore.Qt.Window)
        self.file = None
        self.task_count = 0
        self.codenamecolor_list = []
        self.init_ui()
        print(self)
        
    def init_ui(self):
        self.adjust_window()
        self.read_codes()
        self.init_widgets()
        self.place_blocks()
        self.connect_ui()

    def adjust_window(self):
        self.main_frame = QFrame()
        self.setCentralWidget(self.main_frame)
        self.setWindowTitle("Segmentation app. 1.0::MVP")
        size = QSize(1366, 768)
        self.setMinimumSize(size)
        self.main_layout = QGridLayout()
        self.main_frame.setLayout(self.main_layout)


    def init_widgets(self):
        self.tab_new = tab_widget.my_tab(signal=self.signal_openproject, signal2=self.signal_showall, signal_edittask=self.signal_edittask, parent=self)
        self.higher_control = control_widgets.higher_control(signal1=self.signal_parseprojects, signal2=self.signal_editdescription)
        #self.description = control_widgets.project_description_new(signal=self.signal_editdescription)
        self.description = control_widgets.task_description()
        #self.navigation = control_widgets.view_control(self.signal_showall, self.signal_edittask, self)
        self.navigation = control_widgets.polygon_classes_new(self)
        self.navigation_toolbar = control_widgets.view_toolbar()

    def place_blocks(self):
        self.main_layout.addWidget(self.tab_new, 1, 0, 4, 1)
        self.main_layout.addWidget(self.higher_control, 1, 1)
        self.main_layout.addWidget(self.description, 1, 1)
        self.main_layout.addWidget(self.navigation, 1, 1)
        self.main_layout.addWidget(self.navigation_toolbar, 0, 0)
        self.show_higher_control()

    def connect_ui(self):
        self.signal_parseprojects.connect(self.tab_new.parse_projects)
        self.signal_openproject.connect(self.open_project_routine)
        self.tab_new.currentChanged.connect(self.show_tab_new)
        #self.description.btn_addtask.clicked.connect(self.add_task)
        #self.description.btn_edittask.clicked.connect(self.on_edittask)
        #self.navigation.btn_previous.clicked.connect(self.previous_view)
        #self.navigation.btn_next.clicked.connect(self.next_view)
        #self.navigation.btn_edittask.clicked.connect(self.on_edittask)
        self.navigation_toolbar.previous.triggered.connect(self.previous_view)
        self.navigation_toolbar.next.triggered.connect(self.next_view)
        self.navigation_toolbar.previous.triggered.connect(self.previous_polygons)
        self.navigation_toolbar.next.triggered.connect(self.next_polygons)
        self.signal_edittask.connect(self.on_edittask)
        #self.signal_editdescription.connect(self.on_editdescription)
    
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
        self.navigation_toolbar.setVisible(False)
        self.description.setVisible(True)

    def show_higher_control(self):
        self.higher_control.setVisible(True)
        self.navigation.setVisible(False)
        self.navigation_toolbar.setVisible(False)
        self.description.setVisible(False)

    def show_navigation(self):
        self.higher_control.setVisible(False)
        self.description.setVisible(False)
        self.navigation.setVisible(True)
        self.navigation_toolbar.setVisible(True)

    @pyqtSlot(str)
    def open_project_routine(self, project_path):
        if self.file:
            self.file.close()
        self.file = h5py.File(project_path, 'r+')
        self.task_count = self.file.attrs[classifier.hdfs.TASK_COUNT.value]
        self.tab_new.parse_tasks(self.file)
        #self.description.parse_description(self.file)
        self.tab_new.parse_view(self.file)
        #self.navigation.adjust_pallete(self.file)
        self.navigation.fill()
        self.higher_control.description.updateitem(self.file.attrs[classifier.hdfs.DESCRIPTION.value])
        #self.task_count = self.file.attrs[classifier.hdfs.TASK_COUNT.value]
        #self.tab_new.update_info()
        #print(self.task_count)

    def adjust_opened_project(self):
        self.tab_new.parse_tasks(self.file)
        #self.description.parse_description(self.file)
        self.tab_new.parse_view(self.file)

    def add_task(self):
        #print(classifier.task_attrs.TO_DO.value)
        #"""
        if self.file:
            hdf = self.file
            task = QFileDialog.getOpenFileName()[0]
            if task:
                tasks_count = hdf.attrs[classifier.hdfs.TASK_COUNT.value]
                task_numpy = cv2.imread(task)
                hdf.create_dataset(str(tasks_count), data=task_numpy)
                hdf[str(tasks_count)].attrs[classifier.tasks.STATUS.value] = classifier.tasks.TO_DO.value
                hdf[str(tasks_count)].attrs[classifier.tasks.COUNT.value] = 0
                #hdf[str(tasks_count)].attrs[classifier.task_attrs.STATUS.value] = classifier.task_attrs.TO_DO.value
                #hdf[str(tasks_count)].attrs[classifier.task_attrs.COUNT.value] = 0
                hdf.attrs[classifier.hdfs.TASK_COUNT.value] += 1
                self.adjust_opened_project()
        #"""

    @pyqtSlot(int)
    def on_edittask(self, index=-1):
        current_task = self.tab_new.view_w.current_task()
        if index != -1:
            current_task = index
        self.edit = edit_widgets.edit_widget(index=current_task, main=self, hdf=self.file)
        self.edit.exec_()

    @pyqtSlot(str)
    def on_editdescription(self, newdescription):
        if self.file: #корректно проверяю открыт ли hdf????
            self.file.attrs[classifier.hdfs.DESCRIPTION.value] = newdescription

    def read_codes(self):
        codes = classifier.classes.code()
        names = classifier.classes.name()
        colors= classifier.classes.color()
        for code, name, color in zip(codes, names, colors):
            self.codenamecolor_list.append((code, name, color))

    def on_showall(self):
        print("showall")
        self.signal_showall.emit(1)

    def previous_view(self):
        self.tab_new.change_view(index=-1)

    def next_view(self):
        self.tab_new.change_view(index=+1)

    def previous_polygons(self):
        #self.navigation.tree.change_polygons(index=-1, hdf=self.file)
        self.navigation.update(index=-1)

    def next_polygons(self):
        #self.navigation.tree.change_polygons(index=+1, hdf=self.file)
        self.navigation.update(index=+1)

    def get_name(self, code):
        for triple in self.codenamecolor_list:
            if triple[0] == code:
                return triple[1]

    def get_code(self, name):
        for triple in self.codenamecolor_list:
            if triple[1] == name:
                return triple[0]

    def get_color(self, code):
        for triple in self.codenamecolor_list:
            if triple[0] == code:
                return triple[2]

    
