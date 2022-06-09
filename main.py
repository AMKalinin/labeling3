from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene, QMenuBar)
from PyQt5 import QtWidgets, QtGui, QtCore

import os
import json
import classifier
import utils
import h5py
import time
import re
import cv2
import control
import tab
import edit


class mainWindow(QMainWindow):
    _parse_projects = pyqtSignal()
    _open_project = pyqtSignal(str)
    _show_all = pyqtSignal(int)
    _edit_task = pyqtSignal(int)
    _edit_description = pyqtSignal(str)
    _refresh_tree = pyqtSignal()
    def __init__(self, screen):
        QMainWindow.__init__(self, flags=QtCore.Qt.Window)
        self.screen = screen
        self.file = None
        self.task_count = 0
        self.codenamecolor = []
        self.init_ui()
        
    def init_ui(self):
        self.adjust_window()
        self.init_widgets()
        self.place_blocks()
        self.connect_ui()

    def adjust_window(self):
        self.main_frame = QFrame()
        self.setCentralWidget(self.main_frame)
        self.setWindowTitle("Segmentation app. 1.1::Release")
        self.screen.setHeight(self.screen.height() - 50)
        #self.screen.setWidth(self.screen.width() - 10)
        #print(self.screen)
        #size = QSize(1366, 768)
        self.setMaximumSize(self.screen.size())
        self.setMinimumSize(self.screen.size())
        self.main_layout = QGridLayout()
        self.main_frame.setLayout(self.main_layout)

    def init_widgets(self):
        self.tab = tab.tab(self)
        self.projectControl = control.projectControl(self)
        self.taskDescription = control.taskDescription(self)
        self.viewTree = control.polygonTree(parent=self, main=self)
        self.viewToolbar = control.viewToolbar()

    def place_blocks(self):
        self.main_layout.addWidget(self.tab, 1, 0, 4, 1)
        self.main_layout.addWidget(self.projectControl, 1, 1)
        self.main_layout.addWidget(self.taskDescription, 1, 1)
        self.main_layout.addWidget(self.viewTree, 1, 1)
        #self.main_layout.addWidget(self.viewToolbar, 0, 0)
        self.tab.view_layout.setMenuBar(self.viewToolbar)
        self.show_tab1()

    def connect_ui(self):
        self._parse_projects.connect(self.tab.parse_projects)
        self._open_project.connect(self.on_open_project)
        self.tab.currentChanged.connect(self.show_tab)
        #self.taskDescription.btn_addtask.clicked.connect(self.add_task)
        #self.taskDescription.btn_edit_task.clicked.connect(self.on_edit_task)
        #self.viewTree.btn_previous.clicked.connect(self.previous_view)
        #self.viewTree.btn_next.clicked.connect(self.next_view)
        #self.viewTree.btn_edit_task.clicked.connect(self.on_edit_task)
        self.viewToolbar.previous.triggered.connect(self.previous_view)
        self.viewToolbar.previous.triggered.connect(self.previous_polygons)
        self.viewToolbar.next.triggered.connect(self.next_view)
        self.viewToolbar.next.triggered.connect(self.next_polygons)
        self._edit_task.connect(self.on_edit_task)
        self._refresh_tree.connect(self.viewTree.fill)
        self.viewTree.itemSelectionChanged.connect(self.send_selected)
        #self._edit_description.connect(self.on_edit_description)
     
    def show_tab(self):      
        if self.tab.currentWidget() == self.tab.split:
            self.show_tab2()
        elif self.tab.currentWidget() == self.tab.projects:
            self.show_tab1()
        elif self.tab.currentWidget() == self.tab.view:
            self.show_tab3()

    def show_tab2(self):
        self.projectControl.setVisible(False)
        self.viewTree.setVisible(False)
        self.viewToolbar.setVisible(False)
        self.taskDescription.setVisible(True)

    def show_tab1(self):
        self.projectControl.setVisible(True)
        self.viewTree.setVisible(False)
        self.viewToolbar.setVisible(False)
        self.taskDescription.setVisible(False)

    def show_tab3(self):
        self.projectControl.setVisible(False)
        self.taskDescription.setVisible(False)
        self.viewTree.setVisible(True)
        self.viewToolbar.setVisible(True)

    def send_selected(self):
        items = []
        for item in self.viewTree.selectedItems():
            if self.viewTree.indexOfTopLevelItem(item) == -1:
                items.append(item)
        self.tab.view._selectedItems.emit(items)

    @pyqtSlot(str)
    def on_open_project(self, project_path):
        if self.file:
            self.file.close()
        self.file = h5py.File(project_path, 'r+')
        self.task_count = self.file.attrs[classifier.hdfs.TASK_COUNT.value]
        self.update_codenamecolor()
        self.tab.parse_tasks()
        #self.taskDescription.parse_description(self.file)
        self.tab.parse_view()
        #self.viewTree.adjust_pallete(self.file)
        self.viewTree.fill()
        self.projectControl.description.updateWidgetDescription()
        #self.projectControl.description.updateitem(self.file.attrs[classifier.hdfs.DESCRIPTION.value])
        #self.task_count = self.file.attrs[classifier.hdfs.TASK_COUNT.value]
        #self.tab.update_info()
        #print(self.task_count)

    def adjust_opened_project(self):
        self.tab.parse_tasks()
        #self.taskDescription.parse_description(self.file)
        self.tab.parse_view()

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
    def on_edit_task(self, index=-1):
        current_task = self.tab.view_w.current_task()
        if index != -1:
            current_task = index
        #self.edit = edit.edit_widget(index=current_task, main=self, hdf=self.file)
        self.edit = edit.editWidget(parent=self, main=self, index=current_task)
        self.edit.exec_()

    @pyqtSlot(str)
    def on_edit_description(self, newdescription):
        if self.file: #корректно проверяю открыт ли hdf????
            self.file.attrs[classifier.hdfs.DESCRIPTION.value] = newdescription

    def update_codenamecolor(self):
        self.codenamecolor.clear()
        codes = classifier.classes.code()
        names = classifier.classes.name()
        colors= classifier.classes.color()
        for code, name, color in zip(codes, names, colors):
            if str(code) in self.file.attrs[classifier.hdfs.CLASSES.value]:
                self.codenamecolor.append((code, name, color))

    def on_show_all(self):
        #print("showall")
        self._show_all.emit(1)

    def previous_view(self):
        self.tab.change_view(index=-1)

    def next_view(self):
        self.tab.change_view(index=+1)

    def previous_polygons(self):
        self.viewTree.update(index=-1)

    def next_polygons(self):
        self.viewTree.update(index=+1)

    def get_name(self, code):
        for triple in self.codenamecolor:
            if triple[0] == code:
                return triple[1]

    def get_code(self, name):
        for triple in self.codenamecolor:
            if triple[1] == name:
                return triple[0]

    def get_color(self, code):
        for triple in self.codenamecolor:
            if triple[0] == code:
                return triple[2]
        #if triple[0] == '000':
        if code == 0:
            return 5

    def adjust_code(self, taskindex, itemindex, newcode):
        attr = self.file[str(taskindex)].attrs[str(itemindex)]
        attr = re.sub(r';[0-9][0-9][0-9];', ';' + newcode + ';', attr)
        self.file[str(taskindex)].attrs[str(itemindex)] = attr


    def send_task_index(self, index):
        self.taskDescription.update_aerial(index)

    
