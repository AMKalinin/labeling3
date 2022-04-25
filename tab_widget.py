from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
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


class my_tab(QTabWidget):
    def __init__(self, signal, signal2=None, parent=None, signal_edittask=None):
        super().__init__()
        self.signal = signal
        self.signal2=signal2
        self.signal_edittask = signal_edittask
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
                project_widget = project_widgets.project_widget_new(signal=self.signal, path=project_full_name)
                self.projects_layout.addWidget(project_widget)

    def parse_tasks(self, hdf):
        utils.clear_layout(layout=self.tasksleft_layout)
        utils.clear_layout(layout=self.tasksright_layout)
        tasks_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
        for task_id in range(tasks_count):
            task_status = hdf[str(task_id)].attrs[classifier.HDF_TASK_STATUS]
            if task_status == classifier.HDF_TASK_STATUS_0 or status == classifier.HDF_TASK_STATUS_1:
                task_widget = task_widgets.task_widget_new(project_file=hdf, identifier=task_id, mode=classifier.TASK_WIDGET_MODE_0, signal_edittask=self.signal_edittask)#, signal=self.signal_reopen_project)
                self.tasksleft_layout.addWidget(task_widget)
            elif task_status == classifier.HDF_TASK_STATUS_2 or status == classifier.HDF_TASK_STATUS_3:
                print("creating right")
                #task_widget = task_base.task_widget(path=project_path, identifier=number, mode=classifier.TASK_WIDGET_MODE_1, signal=self.signal_parse_tasks)
                #self.tab_tasks_right_layout.addWidget(task_widget)

    def parse_view(self, hdf):
        #self.view_w = view_widgets.view_project(parent=self.view, file_link=hdf)
        self.view_w.deleteLater()  #!!! ПРОВЕРЯТЬ УДАЛЕНИЕ ВИДЖЕТОВ ПРИ ОБЫЧНОМ ПЕРЕИМЕНОВЫВАНИИ НЕ УНИЧТОЖАЕТСЯ
        self.view_w = view_widgets.view_view(parent=self.view, file_link=hdf, signal=self.signal2) 

    def init_view(self):
        #self.view_w = view_widgets.view_project(parent=self.view, file_link=None)
        self.view_w = view_widgets.view_view(parent=self.view, file_link=None, signal=self.signal2)
    
    def change_view(self, index):
        self.view_w.change_pixmap(index)