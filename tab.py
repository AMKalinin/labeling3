from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene)
from PyQt5 import QtWidgets, QtGui, QtCore


import project
import task
import view
import os
import json
import classifier
import utils
import h5py
import time
import re
import cv2

class viewFrame(QWidget):
    _selectedItems = pyqtSignal(list)
    def __init__(self, parent):
        super().__init__(parent=parent)


class tab(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.main = parent
        self.view_w = None

        self.init_ui()
        self.parse_projects()
        self.init_view()

    def init_ui(self):
        self.init_areas()
        self.init_layouts()
        self.set_layouts()
        self.place_tabs()

    def init_layouts(self):
        self.projects_layout = QVBoxLayout()
        self.tasksleft_layout = QVBoxLayout()
        self.tasksright_layout = QVBoxLayout()
        self.view_layout = QGridLayout()

    def init_areas(self):
        self.projects = QScrollArea(self)
        self.tasksleft = QScrollArea(self)
        self.tasksright = QScrollArea(self)
        self.view = viewFrame(self)
        #self.view._selectedItems = pyqtSignal(list)

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
        utils.clear_layout(self.projects_layout)
        names = os.listdir(classifier.items.PROJECTS.value)
        for name in names:
            path = classifier.items.PROJECTS.value + name
            widget = project.projectWidget(path=path, parent=self, main=self.main)
            self.projects_layout.addWidget(widget)

    def parse_tasks(self):
        utils.clear_layout(layout=self.tasksleft_layout)
        utils.clear_layout(layout=self.tasksright_layout)
        for index in range(self.main.task_count):
            self.create_task(index)

    def create_task(self, index, task_old=None):
        if task_old != None:
            task_old.deleteLater()
        status = self.main.file[str(index)].attrs[classifier.tasks.STATUS.value]
        if status == classifier.tasks.TO_DO.value or status == classifier.tasks.IN_PROGRESS.value:
            widget = task.taskWidget(parent=self, main=self.main, index=index, mode=classifier.tasks.LEFT.value)
            self.tasksleft_layout.addWidget(widget)
        elif status == classifier.tasks.TO_CHECK.value:  # or status == classifier.HDF_TASK_STATUS_3:
            widget = task.taskWidget(parent=self, main=self.main, index=index, mode=classifier.tasks.RIGHT.value)
            self.tasksright_layout.addWidget(widget)

    def parse_view(self):
        self.view_w.deleteLater()  #!!! ПРОВЕРЯТЬ УДАЛЕНИЕ ВИДЖЕТОВ ПРИ ОБЫЧНОМ ПЕРЕИМЕНОВЫВАНИИ НЕ УНИЧТОЖАЕТСЯ
        self.view_w = view.baseView(main=self.main, parent=self.view)
        self.view._selectedItems.connect(self.view_w.show_shapes)

    def init_view(self):
        self.view_w = view.baseView(main=self.main, parent=self.view)
    
    def change_view(self, index):
        self.view_w.change_background(index)