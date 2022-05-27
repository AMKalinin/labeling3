from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene, QToolBar, QTreeWidget, QTreeWidgetItem)
from PyQt5 import QtWidgets, QtGui, QtCore

import new_project
import project_widgets
import task_widgets
import view_widgets
import select_classes as tree
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

        self.name = QListWidgetItem(classifier.hdfs.NAME.value + self.name)
        self.classes = QListWidgetItem(classifier.hdfs.CLASSES.value + self.classes)
        self.time_c = QListWidgetItem(classifier.hdfs.TIME_C.value + self.time_c)
        self.time_u = QListWidgetItem(classifier.hdfs.TIME_U.value + self.time_u)
        self.description = QListWidgetItem(classifier.hdfs.DESCRIPTION.value + self.description)
        self.task_count = QListWidgetItem(classifier.hdfs.TASK_COUNT.value + self.task_count)

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
        self.name.setText(classifier.hdfs.NAME.value + hdf.attrs[classifier.hdfs.NAME.value])
        self.description.setText(classifier.hdfs.DESCRIPTION.value + hdf.attrs[classifier.hdfs.DESCRIPTION.value])
        self.task_count.setText(classifier.hdfs.TASK_COUNT.value +  str(hdf.attrs[classifier.hdfs.TASK_COUNT.value])) #str?
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

class getdescription(QDialog):
    def __init__(self, signal, parent=None):
        super().__init__()
        self.signal = signal
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.line = QLineEdit()
        self.layout.addWidget(self.line)
        self.line.textChanged.connect(self.mysignal)

    def mysignal(self):
        text = self.line.text()
        self.signal.emit(text)


class mydescription(QListWidget):
    def __init__(self, signal1, signal2, parent=None):
        super().__init__()
        self.signal1 = signal1
        self.signal2 = signal2
        self.setMouseTracking(True)
        self.setMaximumSize(300, 300)
        self.addItem("Описание проекта")
        self.item = self.item(0)
        self.itemDoubleClicked.connect(self.on_dc)
        self.signal2.connect(self.updateitem)

    def enterEvent(self, event):
        print("enterEvent")
    
    def leaveEvent(self, event):
        print("leaveEvent")

    def on_dc(self):
        print("double clicked")
        a = getdescription(self.signal2)
        a.exec_()
        self.signal1.emit()
    
    def updateitem(self, text):
        self.item.setText(text)

class task_description(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        
        #self.adjust_window()
        self.set_layouts()
        self.init_widgets()
        self.fill_layouts()
    
    def adjust_window(self):
        pass
        #self.setMaximumSize(300, 300)       

    def set_layouts(self):
        self.layout = QGridLayout()
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.left, 1, 0)
        self.layout.addLayout(self.right, 1, 1)

    def init_widgets(self):
        self.save = QPushButton("Сохранить")
        self.discard = QPushButton("Отменить редактирование")

        self.line0 = QLineEdit()
        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()
        self.line5 = QLineEdit()
        self.line6 = QLineEdit()
        self.line7 = QLineEdit()

    def fill_layouts(self):
        self.left.addWidget(QLabel('0'))
        self.left.addWidget(QLabel('1'))
        self.left.addWidget(QLabel('2'))
        self.left.addWidget(QLabel('3'))
        self.left.addWidget(QLabel('4'))
        self.left.addWidget(QLabel('5'))
        self.left.addWidget(QLabel('6'))
        self.left.addWidget(QLabel('7'))

        self.right.addWidget(self.line0)
        self.right.addWidget(self.line1)
        self.right.addWidget(self.line2)
        self.right.addWidget(self.line3)
        self.right.addWidget(self.line4)
        self.right.addWidget(self.line5)
        self.right.addWidget(self.line6)
        self.right.addWidget(self.line7)

        self.layout.addWidget(self.save, 2, 1)
        self.layout.addWidget(self.discard, 2, 0)
        self.layout.addWidget(QLabel("Параметры снимка:"), 0, 0)


class higher_control(QGroupBox):
    def __init__(self, signal1, signal2, parent=None):
        super().__init__()
        self.signal1 = signal1
        self.signal2 = signal2
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
        self.layout.addWidget(self.description)

    def init_content(self):
        self.btn_new = QPushButton("Создать новый файл проекта")
        self.btn_add = QPushButton("Добавить проект из ...")
        self.btn_based = QPushButton("Создать проект на основе существующего")
        self.init_description()
        

    def init_description(self):
        #self.description = QListWidget()
        #self.description.setMouseTracking(True)
        #self.description.itemEntered.connect(self.test)
        #btn_qsize = self.btn_based.size()
        #btn_width = btn_qsize.width()
        #self.description.setMaximumSize(btn_width, 300)
        #self.description.setMaximumSize(100, 300)
        self.description = mydescription(signal1=self.signal1, signal2=self.signal2)


    #def test(self):
    #    print("item entered")

    def connect_ui(self):
        self.btn_new.clicked.connect(self.on_new)

    def on_new(self):
        self.dialog = new_project.new_project_dialog_new(signal=self.signal1)
        #self.dialog = segflex_classes_choose.classes_choose_new()
        self.dialog.exec_()
        #self.dialog.show()
        #print(self.dialog.selected.chosen)
        #print(self.dialog.selected.chosen) #????? виджет почему имеет доступ к атрибуту после удаления????
        #self.dialog.deleteLater()
        #print(self.dialog.selected.chosen) #????? виджет почему имеет доступ к атрибуту после удаления????
        #self.dialog.exec_()

class view_toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__()

        self.add_actions()

    def init_widgets(self):
        self.first = QToolButton()
        self.first.setIcon(QIcon('__icons__/cancel_tbtn.png'))

    def add_actions(self):
        self.first = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'go to first image in project')
        self.previous = self.addAction(QIcon('__icons__/previous_tbtn.png'), 'go to previous image in project')
        self.next = self.addAction(QIcon('__icons__/next_tbtn.png'), 'go to next image in project')
        self.last = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'go to last image in project')
        self.add = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'add new image to project')
        self.delete = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'delete image from project')
        self.showall = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'set all polygons in list as selected')
        self.hideall = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'set all polygons in list as deselected')

class view_control(QGroupBox):
    def __init__(self, signal_showall, signal_edittask, parent=None):
        super().__init__(parent=parent)
        self.signal_showall = signal_showall
        self.signal_edittask = signal_edittask
        #self.create_pallete()
        self.init_ui()
        self.tree = polygon_classes(parent)
        self.layout.addWidget(self.tree)
        

    def init_ui(self):
        """
        self.btn_previous = QPushButton("<<")
        self.btn_next = QPushButton(">>")
        self.btn_showall = QPushButton("show all")
        self.btn_showall.clicked.connect(self.on_showall)
        self.btn_hideall = QPushButton("hide all")
        self.btn_hideall.clicked.connect(self.on_hideall)
        self.btn_edittask = QPushButton("edit task")
        self.btn_edittask.clicked.connect(self.on_edittask)
        """

        self.layout = QVBoxLayout()
        """"
        self.layout.addWidget(self.btn_previous)
        self.layout.addWidget(self.btn_next)
        self.layout.addWidget(self.btn_showall)
        self.layout.addWidget(self.btn_hideall)
        self.layout.addWidget(self.btn_edittask)
        self.layout.addWidget(self.list)
        """
        self.setLayout(self.layout)
    
    def on_showall(self):
        self.signal_showall.emit(1)

    def on_hideall(self):
        self.signal_showall.emit(-1)

    def on_edittask(self):
        self.signal_edittask.emit(-1)

    """

    def create_pallete(self):
        color_index = 2
        self.list = QListWidget()
        for cclass in classifier.classes:
            pixmap = QPixmap(50,50)
            color = QColor(Qt.GlobalColor(color_index))
            pixmap.fill(color)
            self.list.addItem(QListWidgetItem(QIcon(pixmap), str(cclass.value[1]) + " " +str(cclass.value[3])))
            color_index += 1
            if color_index == 19:
                color_index = 2

    def adjust_pallete(self, hdf):
        color_index = 2
        self.layout.removeWidget(self.list)
        self.list.deleteLater()
        self.list = QListWidget()
        for cclass in hdf.attrs[classifier.hdfs.CLASSES.value]:
            pixmap = QPixmap(50,50)
            color = QColor(Qt.GlobalColor(color_index))
            pixmap.fill(color)
            self.list.addItem(QListWidgetItem(QIcon(pixmap), cclass))
            color_index += 1
            if color_index == 19:
                color_index = 2

        self.layout.addWidget(self.list)
    """

#class view_control_new(QGroupBox):


class polygon_classes_new(QTreeWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.index = 0
    
        self.setColumnCount(4)
        self.setHeaderLabels(['Name', 'Code', 'Index', 'Points'])
        self.setMaximumSize(200, 400)

    def update(self, index):
        self.index += index
        if self.index < 0:
            self.index = 0
        elif self.index > self.parent.task_count - 1:
            self.index = self.parent.task_count - 1
        self.fill()

    def fill(self):
        self.clear()
        for code in self.parent.file.attrs[classifier.hdfs.CLASSES.value]:
            name = self.parent.get_name(int(code))
            self.addTopLevelItem(QTreeWidgetItem([name, code, '', '']))

        for name, value in self.parent.file[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                attr_class = utils.attrs_get_class(value)
                attr_points = utils.attrs_get_points(value)
                for index in range(self.topLevelItemCount()):
                    if self.topLevelItem(index).text(1) == attr_class:
                        self.topLevelItem(index).addChild(QTreeWidgetItem(['', attr_class, name, attr_points]))




