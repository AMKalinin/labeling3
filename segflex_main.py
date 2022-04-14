from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene)
from PyQt5 import QtWidgets, QtGui, QtCore

import segflex_new_project
import segflex_project_as_widget as project
import segflex_task_as_widget as task_base
import segflex_seg_window as seg
import segflex_seg_label as seg_label
import os
import json
import segflex_classifier as classifier
import segflex_utils as utils
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

        self.btn_add = QPushButton("Добавить задачу")

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
        self.layout.addWidget(self.btn_add)

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
        self.dialog = segflex_new_project.new_project_dialog_new(signal=self.signal)
        self.dialog.exec_()

class my_tab(QTabWidget):
    def __init__(self, signal, parent=None):
        super().__init__()
        self.signal = signal
        self.index = 0
        self.view_w = None

        self.init_ui()
        self.parse_projects()
        self.init_view()

    def init_ui(self):
        self.init_tabs()
        self.init_layouts()
        self.set_layouts()
        self.place_tabs()

    def init_layouts(self):
        self.projects_layout = QVBoxLayout()
        self.tasksleft_layout = QVBoxLayout()
        self.tasksright_layout = QVBoxLayout()
        self.view_layout = QGridLayout()

    def init_tabs(self):
        self.projects = QScrollArea(self)
        self.tasksleft = QScrollArea(self)
        self.tasksright = QScrollArea(self)
        self.view = QWidget(self) 

        self.projects.setWidgetResizable(True)
        self.tasksleft.setWidgetResizable(True)
        self.tasksright.setWidgetResizable(True)

        self.split = QSplitter()
        self.split.addWidget(self.tasksleft)
        self.split.addWidget(self.tasksright)

        self.projects_group = QGroupBox(self.projects)
        self.tasksleft_group = QGroupBox(self.tasksleft)
        self.tasksright_group = QGroupBox(self.tasksright)

        self.projects_group.setTitle("Проекты")
        self.tasksleft_group.setTitle("Разметка")
        self.tasksright_group.setTitle("Контроль и редактирование")

        self.projects.setWidget(self.projects_group)
        self.tasksleft.setWidget(self.tasksleft_group)
        self.tasksright.setWidget(self.tasksright_group)

    def set_layouts(self):
        self.projects_group.setLayout(self.projects_layout)
        self.tasksleft_group.setLayout(self.tasksleft_layout)
        self.tasksright_group.setLayout(self.tasksright_layout)
        self.view.setLayout(self.view_layout)

    def place_tabs(self):
        self.addTab(self.projects, "Проекты")
        self.addTab(self.split, "Задачи")
        self.addTab(self.view, "Просмотр")

    def parse_projects(self):
        utils.clear_layout(layout=self.projects_layout)
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        for project_short_name in projects_list:
            project_full_name = classifier.PROJECTS_FOLDER_FULL_NAME + '/' + project_short_name
            with h5py.File(project_full_name, 'r') as hdf:
                project_widget = project.project_widget_new(signal=self.signal, path=project_full_name)
                self.projects_layout.addWidget(project_widget)

    def parse_tasks(self, hdf):
        utils.clear_layout(layout=self.tasksleft_layout)
        utils.clear_layout(layout=self.tasksright_layout)
        tasks_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
        for task_id in range(tasks_count):
            task_status = hdf[str(task_id)].attrs[classifier.HDF_TASK_STATUS]
            if task_status == classifier.HDF_TASK_STATUS_0 or status == classifier.HDF_TASK_STATUS_1:
                task_widget = task_base.task_widget_new(project_file=hdf, identifier=task_id, mode=classifier.TASK_WIDGET_MODE_0)#, signal=self.signal_reopen_project)
                self.tasksleft_layout.addWidget(task_widget)
            elif task_status == classifier.HDF_TASK_STATUS_2 or status == classifier.HDF_TASK_STATUS_3:
                print("creating right")
                #task_widget = task_base.task_widget(path=project_path, identifier=number, mode=classifier.TASK_WIDGET_MODE_1, signal=self.signal_parse_tasks)
                #self.tab_tasks_right_layout.addWidget(task_widget)

    def parse_view(self, hdf):
        self.view_w = seg_label.view_project(parent=self.view, file_link=hdf)    

    def init_view(self):
        self.view_w = seg_label.view_project(parent=self.view, file_link=None)
    
    def change_view(self, index):
        self.view_w.change_pixmap(index)

class view_control(QGroupBox):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.btn_previous = QPushButton("<<")
        self.btn_next = QPushButton(">>")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_previous)
        self.layout.addWidget(self.btn_next)

        self.setLayout(self.layout)

class main_window(QMainWindow):
    signal_parse_projects = pyqtSignal()
    signal_open_project = pyqtSignal(str)
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        self.file = None
        self.init_ui()
        
    def init_ui(self):
        self.adjust_window()
        utils.check_create_projects_folder()
        self.check_create_projects_folder()
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

    def check_create_projects_folder(self):
        if not os.path.exists(classifier.PROJECTS_FOLDER_FULL_NAME):
            os.mkdir(classifier.PROJECTS_FOLDER_FULL_NAME)

    def init_widgets(self):
        self.tab_new = my_tab(signal=self.signal_open_project)
        self.higher_control = higher_control(signal=self.signal_parse_projects)
        self.description = project_description_new()
        self.navigation = view_control()

    def place_blocks(self):
        self.main_layout.addWidget(self.tab_new, 0, 0, 4, 1)
        self.main_layout.addWidget(self.higher_control, 0, 1)
        self.main_layout.addWidget(self.description, 0, 1)
        self.main_layout.addWidget(self.navigation, 0, 1)
        self.show_higher_control()

    def connect_ui(self):
        self.signal_parse_projects.connect(self.tab_new.parse_projects)
        self.signal_open_project.connect(self.open_project_routine)
        self.tab_new.currentChanged.connect(self.show_tab_new)
        self.description.btn_add.clicked.connect(self.add_task)
        self.navigation.btn_previous.clicked.connect(self.previous_view)
        self.navigation.btn_next.clicked.connect(self.next_view)
    
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

    def adjust_opened_project(self):
        self.tab_new.parse_tasks(self.file)
        self.description.parse_description(self.file)
        self.tab_new.parse_view(self.file)

    def project_create_routine(self):
        dialog = segflex_new_project.new_project_dialog_new(signal=self.signal_parse_projects)
        dialog.exec_()

    def add_task(self):
        if self.file:
            hdf = self.file
            task = QFileDialog.getOpenFileName()[0]
            if task:
                tasks_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
                task_numpy = cv2.imread(task)
                hdf.create_dataset(str(tasks_count), data=task_numpy)
                hdf[str(tasks_count)].attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_0
                hdf[str(tasks_count)].attrs[classifier.HDF_TASK_POLYGON_COUNT] = 0
                hdf.attrs[classifier.HDF_FILE_TASK_COUNT] += 1
                self.adjust_opened_project()

    def previous_view(self):
        self.tab_new.change_view(index=-1)

    def next_view(self):
        self.tab_new.change_view(index=+1)
