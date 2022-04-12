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
        self.project_path = project_path
        self.file = project_file
        self.signal = signal
        self.file_name = 'не задано'
        self.file_classes = 'не задано'
        self.file_time_c = 'не задано'
        self.file_time_u = 'не задано'
        self.file_description = 'не задано'
        self.file_task_count = 'не задано'
        self.item_name = QListWidgetItem(classifier.HDF_FILE_NAME + self.file_name)
        self.item_classes = QListWidgetItem(classifier.HDF_FILE_CLASSES + self.file_classes)
        self.item_time_c = QListWidgetItem(classifier.HDF_FILE_TIME_C + self.file_time_c)
        self.item_time_u = QListWidgetItem(classifier.HDF_FILE_TIME_U + self.file_time_u)
        self.item_description = QListWidgetItem(classifier.HDF_FILE_DESCRIPTION + self.file_description)
        self.item_task_count = QListWidgetItem(classifier.HDF_FILE_TASK_COUNT + self.file_task_count)
        self.items_menu = QListWidget()
        self.items_menu.addItem(self.item_name)
        self.items_menu.addItem(self.item_classes)
        self.items_menu.addItem(self.item_time_c)
        self.items_menu.addItem(self.item_time_u)
        self.items_menu.addItem(self.item_description)
        self.items_menu.addItem(self.item_task_count)

        self.btn_add = QPushButton("Добавить задачу")
        self.btn_add.clicked.connect(self.on_add)

        layout = QVBoxLayout()
        layout.addWidget(self.items_menu)
        layout.addWidget(self.btn_add)
        self.setLayout(layout)
        if self.file:
            self.update_description()
    
    def on_add(self):
        task_to_add = QFileDialog.getOpenFileName()[0]
        hdf = self.file
        if task_to_add:
            task_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
            task_as_numpy = cv2.imread(task_to_add)
            hdf.create_dataset(str(task_count), data=task_as_numpy)
            hdf[str(task_count)].attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_0
            hdf[str(task_count)].attrs[classifier.HDF_TASK_POLYGON_COUNT] = 0
            hdf.attrs[classifier.HDF_FILE_TASK_COUNT] += 1
            self.signal.emit()


    def update_description(self):
        hdf = self.file
        self.file_name = hdf.attrs[classifier.HDF_FILE_NAME]
        self.file_classes = hdf.attrs[classifier.HDF_FILE_CLASSES]
        self.file_time_c = hdf.attrs[classifier.HDF_FILE_TIME_C]
        self.file_time_u = hdf.attrs[classifier.HDF_FILE_TIME_U]
        self.file_description = hdf.attrs[classifier.HDF_FILE_DESCRIPTION]
        self.file_task_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
        self.item_name.setText(classifier.HDF_FILE_NAME + self.file_name)
        #self.item_classes.setText(classifier.HDF_FILE_CLASSES + self.file_classes)
        #self.item_time_u.setText(classifier.HDF_FILE_TIME_U + self.file_time_u)
        self.item_description.setText(classifier.HDF_FILE_DESCRIPTION + self.file_description)
        self.item_task_count.setText(classifier.HDF_FILE_TASK_COUNT + str(int(self.file_task_count)))

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



class main_window(QMainWindow):
    signal_parse_tasks = pyqtSignal(str)
    signal_task_index = pyqtSignal(int)

    signal_parse_projects = pyqtSignal()
    signal_open_project = pyqtSignal(str)
    signal_reopen_project = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        self.file = None
        self.init_ui()
        
    def init_ui(self):
        self.adjust_window()
        self.check_create_projects_folder()
        self.init_layouts()
        self.init_widgets()
        self.set_layouts()
        self.place_blocks()
        self.connect_ui()
        self.parse_projects_folder()
        #self.show_view_tab(project_path="/home/iakhmetev/Документы/8.3_version_2_data_labeling/__projects/123.hdf5")

    def adjust_window(self):
        self.main_frame = QFrame()
        self.setCentralWidget(self.main_frame)
        self.setWindowTitle("Segmentation app. 0.9")
        self.resize(1024, 600)

    def check_create_projects_folder(self):
        if not os.path.exists(classifier.PROJECTS_FOLDER_FULL_NAME):
            os.mkdir(classifier.PROJECTS_FOLDER_FULL_NAME)

    def init_layouts(self):
        self.main_layout = QGridLayout()
        self.tab_projects_layout = QVBoxLayout()
        self.tab_tasks_left_layout = QVBoxLayout()
        self.tab_tasks_right_layout = QVBoxLayout()
        self.tab_view_layout = QGridLayout()
        self.view_project_control_layout = QVBoxLayout() #self.view_control_layout = QVBoxLayout()
        self.view_control_layout = QVBoxLayout()

    def init_widgets(self):
        self.init_table()
        self.higher_control = higher_control(signal=self.signal_parse_projects)
        self.description = project_description_new()
        self.navigation = seg_label.view_project_control()

    def set_layouts(self):
        self.main_frame.setLayout(self.main_layout)
        self.tab_projects_group.setLayout(self.tab_projects_layout)
        self.tab_tasks_left_group.setLayout(self.tab_tasks_left_layout)
        self.tab_tasks_right_group.setLayout(self.tab_tasks_right_layout)
        self.tab_view.setLayout(self.tab_view_layout)

    def place_blocks(self):
        self.tab.addTab(self.tab_projects_area, "Проекты")
        self.tab.addTab(self.tab_split, "Задачи")
        self.tab.addTab(self.tab_view, "Просмотр")

        self.main_layout.addWidget(self.tab, 0, 0, 4, 1)
        self.main_layout.addWidget(self.higher_control, 0, 1)
        self.main_layout.addWidget(self.description, 0, 1)
        self.main_layout.addWidget(self.navigation, 0, 1)
        self.show_higher_control()

    def connect_ui(self):
        self.signal_parse_tasks.connect(self.parse_tasks)
        self.signal_parse_projects.connect(self.parse_projects_folder)
        self.signal_open_project.connect(self.open_project_routine)
        self.signal_reopen_project.connect(self.reopen_project_routine)
        self.tab.currentChanged.connect(self.show_tab)
        #self.btn_add_image.clicked.connect(self.on_add_new_task)
    
    def show_tab(self):
        if self.tab.currentWidget() == self.tab_split:
            self.show_description()
        elif self.tab.currentWidget() == self.tab_projects_area:
            self.show_higher_control()
        elif self.tab.currentWidget() == self.tab_view:
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
        print("navigation tab")
        self.higher_control.setVisible(False)
        
        self.description.setVisible(False)
        self.navigation.setVisible(True)

    def init_table(self):
        self.tab = QTabWidget()
        self.tab_projects_area = QScrollArea(self)
        self.tab_tasks_left_area = QScrollArea(self)
        self.tab_tasks_right_area = QScrollArea(self)
        self.tab_view = QWidget(self) #seg.seg_window(path="/home/iakhmetev/Документы/8.3_version_2_data_labeling/__projects/123.hdf5") #QWidget(self)


        self.tab_projects_area.setWidgetResizable(True)
        self.tab_tasks_left_area.setWidgetResizable(True)
        self.tab_tasks_right_area.setWidgetResizable(True)

        self.tab_split = QSplitter()
        self.tab_split.addWidget(self.tab_tasks_left_area)
        self.tab_split.addWidget(self.tab_tasks_right_area)

        self.tab_projects_group = QGroupBox(self.tab_projects_area)
        self.tab_tasks_left_group = QGroupBox(self.tab_tasks_left_area)
        self.tab_tasks_right_group = QGroupBox(self.tab_tasks_right_area)
        self.view = QWidget(self.tab_view)
        #self.tab_view_group = QGroupBox(self.tab_view_widget)

        self.tab_projects_group.setTitle("Проекты")
        self.tab_tasks_left_group.setTitle("Разметка")
        self.tab_tasks_right_group.setTitle("Контроль и редактирование")
        #self.tab_view_group.setTitle("Просмотр задач и маски")

        self.tab_projects_area.setWidget(self.tab_projects_group)
        self.tab_tasks_left_area.setWidget(self.tab_tasks_left_group)
        self.tab_tasks_right_area.setWidget(self.tab_tasks_right_group)
        #self.tab_view_widget.setWidget(self.tab_view_group)

    def on_create_new_project_clicked(self):
        self.dialog = segflex_new_project.new_project_dialog(signal=self.signal_parse_projects)
        self.dialog.exec_()


    def parse_projects_folder(self):
        #self.show_controls_projects()
        self.clear_table_layout(layout=self.tab_projects_layout)
        self.tab.setCurrentWidget(self.tab_projects_area)
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        for project_short_name in projects_list:
            if project_short_name.find(classifier.HDF_POSTFIX) != -1:
                project_full_name = classifier.PROJECTS_FOLDER_FULL_NAME + '/' + project_short_name
                with h5py.File(project_full_name, 'r') as hdf:
                    project_name = hdf.attrs[classifier.HDF_FILE_NAME]
                    project_classes = hdf.attrs[classifier.HDF_FILE_CLASSES]
                    #project_widget = project.project_as_widget(name=project_name, classes=project_classes, path=project_full_name, signal= self.signal_parse_tasks, signal_open=self.signal_open_project)
                    project_widget = project.project_widget_new(signal=self.signal_open_project, path=project_full_name, name=project_name)
                    self.tab_projects_layout.addWidget(project_widget)

    def parse_tasks(self, project_path):
        self.clear_table_layout(layout=self.tab_tasks_left_layout)
        self.clear_table_layout(layout=self.tab_tasks_right_layout)
        #self.tab.setCurrentWidget(self.tab_split)
        self.btn_description.update_description(project_path)
        self.project_path = project_path
        with h5py.File(project_path, 'r') as hdf: #ATTRS???
            self.show_controls_tasks(hdf.attrs[classifier.HDF_FILE_DESCRIPTION])
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            print(type(group_srcs))
            number_of_images = len(group_srcs.keys())
            for number in range(number_of_images):
                status = group_srcs[str(number)].attrs[classifier.HDF_TASK_STATUS]
                print(type(status))
                if status == classifier.HDF_TASK_STATUS_0 or status == classifier.HDF_TASK_STATUS_1:
                    task_widget = task_base.task_widget(path=project_path, identifier=number, mode=classifier.TASK_WIDGET_MODE_0, signal=self.signal_parse_tasks)
                    self.tab_tasks_left_layout.addWidget(task_widget)
                if status == classifier.HDF_TASK_STATUS_2 or status == classifier.HDF_TASK_STATUS_3:
                    task_widget = task_base.task_widget(path=project_path, identifier=number, mode=classifier.TASK_WIDGET_MODE_1, signal=self.signal_parse_tasks)
                    self.tab_tasks_right_layout.addWidget(task_widget)
    
    def show_view_tab(self, project_path):
        hdf = h5py.File(project_path, 'r')
        self.view = seg_label.view_project(parent=self.tab_view, file_link=hdf, signal=self.signal_task_index)
        control = seg_label.view_project_control(signal=self.signal_task_index)
        self.view_project_control_layout.addWidget(control)
        #self.btns_group_open.setVisible(False)
        self.main_layout.addWidget(control, 0, 1)
    
    def view_parse_routine(self):
        print("view parse, file = ", self.file)
        self.view = seg_label.view_project(parent=self.tab_view, file_link=self.file, signal=self.signal_task_index)


    @pyqtSlot(str)
    def open_project_routine(self, project_path):
        #print(project_path)
        #print("open")
        if self.file:
            self.file.close()
            #print(self.file)
            #if not self.file.closed:
                #self.file.close()
                #print(self.file.closed)
        #self.file_path = project_path
        self.file = h5py.File(project_path, 'r+')
        self.help_clear_layouts()
        self.task_parse_routine()#, path=project_path)
        self.description_parse_routine()
        self.view_parse_routine()

        #self.btn_add_task_create()
        #self.view.deleteLater()
        #print(self.view)

        #self.parse_tasks(project_path)
        #self.show_view_tab(project_path)
    @pyqtSlot()
    def reopen_project_routine(self):
        self.help_clear_layouts()
        self.task_parse_routine()
        self.descriptrion_reparse_routine()

    def project_create_routine(self):
        dialog = segflex_new_project.new_project_dialog_new(signal=self.signal_parse_projects)
        dialog.exec_()

    def description_parse_routine(self):
        #hdf = self.file
        #utils.clear_layout(self.tasks_control_layout)
        #self.description.deleteLater()
        self.description = project_description_new(project_file=self.file, signal=self.signal_reopen_project)
        #self.description.update_description(hdf)
        self.main_layout.addWidget(self.description, 0, 1)
        #self.tasks_control_layout.addWidget(self.description)

    def descriptrion_reparse_routine(self):
        #hdf = self.file
        #self.description.update_description(hdf)
        #self.description.deleteLater()
        self.description = project_description_new(project_file=self.file, signal=self.signal_reopen_project)
        self.main_layout.addWidget(self.description, 0, 1)

    def task_parse_routine(self):
        hdf = self.file
        number_of_images = len(hdf.keys())
        for number in range(number_of_images):
            status = hdf[str(number)].attrs[classifier.HDF_TASK_STATUS]
            if status == classifier.HDF_TASK_STATUS_0 or status == classifier.HDF_TASK_STATUS_1:
                task_widget = task_base.task_widget_new(project_file=hdf, identifier=number, mode=classifier.TASK_WIDGET_MODE_0, signal=self.signal_reopen_project)
                self.tab_tasks_left_layout.addWidget(task_widget)
            if status == classifier.HDF_TASK_STATUS_2 or status == classifier.HDF_TASK_STATUS_3:
                print("creating right")
                #task_widget = task_base.task_widget(path=project_path, identifier=number, mode=classifier.TASK_WIDGET_MODE_1, signal=self.signal_parse_tasks)
                #self.tab_tasks_right_layout.addWidget(task_widget)


    def clear_table_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
            #layout.itemAt(i).widget().deleteLater()


    def check_create_projects_folder(self):
        if not os.path.exists(classifier.PROJECTS_FOLDER_FULL_NAME):
            os.mkdir(classifier.PROJECTS_FOLDER_FULL_NAME)

    def help_clear_layouts(self):
        utils.clear_layout(self.tab_tasks_left_layout)
        utils.clear_layout(self.tab_tasks_right_layout)
        #utils.clear_layout(self.tasks_control_layout)
        utils.clear_layout(self.view_control_layout)

