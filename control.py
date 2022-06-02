from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene, QToolBar,
                            QTreeWidget, QTreeWidgetItem, QListView, QAbstractItemView                 )
from PyQt5 import QtWidgets, QtGui, QtCore

import dialog
import os
import classifier
import dialog
import utils
import h5py
import time
import re
import cv2

class newDescription(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.parent = parent
        self.setWindowTitle("Введите новое описание проекта:")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.line = QLineEdit()
        self.layout.addWidget(self.line)
        self.line.textChanged.connect(self.parent.updateFileDescription)

class editDescription(QListWidget):
    def __init__(self, parent, main):
        super().__init__(parent=parent)
        self.main = main

        self.setMouseTracking(True)
        #self.setMaximumSize(300, 300)
        self.addItem("Описание проекта")
        self.item = self.item(0)
        self.itemDoubleClicked.connect(self.on_doubleclick)

    def enterEvent(self, event):
        pass #подсветка при наводке
    
    def leaveEvent(self, event):
        pass

    def on_doubleclick(self):
        getdescription = newDescription(self)
        getdescription.exec_()
        self.main._parse_projects.emit()
    
    def updateFileDescription(self, text):
        self.main.file.attrs[classifier.hdfs.DESCRIPTION.value] = text
        self.updateWidgetDescription()
        if not text:
            self.item.setText("Описание проекта")
    
    def updateWidgetDescription(self):
        self.item.setText(self.main.file.attrs[classifier.hdfs.DESCRIPTION.value])


class projectControl(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.main = parent
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
        self.layout.addWidget(self.new)
        self.layout.addWidget(self.add)
        self.layout.addWidget(self.based)
        self.layout.addWidget(self.description)

    def init_content(self):
        self.new = QPushButton("Создать новый файл проекта")
        self.add = QPushButton("Добавить проект из ...")
        self.based = QPushButton("Создать проект на основе существующего")
        self.description = editDescription(parent=self, main=self.main)

    def connect_ui(self):
        self.new.clicked.connect(self.on_new)
        self.based.clicked.connect(self.on_based)

    def on_new(self):
        self.dialog = dialog.newProject(self.main)
        self.dialog.exec_()
        

    def on_based(self):
        file_dialog_response = QFileDialog.getOpenFileName()[0]

        if file_dialog_response[-5:] == classifier.hdfs.POSTFIX.value:
            self.dialog = dialog.basedProject(main = self.main, old_hdf=file_dialog_response)
            self.dialog.exec_()
        else:
            message = QMessageBox.about(self, "Ошибка:", "Неправильный тип файла")

class taskDescription(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        
        self.adjust_window()
        self.set_layouts()
        self.init_widgets()
        self.fill_layouts()
    
    def adjust_window(self):
        pass    

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


class polygonTree(QTreeWidget):
    def __init__(self, main, parent):
        super().__init__(parent=parent)
        self.main = main
        self.index = 0
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setColumnCount(4)
        self.setHeaderLabels(['Name', 'Code', 'Index', 'Points'])
        self.setMaximumSize(200, 400)

    def update(self, index):
        self.index += index
        if self.index < 0:
            self.index = 0
        elif self.index > self.main.task_count - 1:
            self.index = self.main.task_count - 1
        self.fill()

    def fill(self):
        self.clear()
        for code in self.main.file.attrs[classifier.hdfs.CLASSES.value]:
            name = self.main.get_name(int(code))
            self.addTopLevelItem(QTreeWidgetItem([name, code, '', '']))
        self.addTopLevelItem(QTreeWidgetItem(['ВЫБРАТЬ КЛАСС', '000', '', '']))

        for name, value in self.main.file[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                attr_class = utils.attrs_get_class(value)
                attr_points = utils.attrs_get_points(value)
                attr_color = self.main.get_color(int(attr_class))
                attr_color = Qt.GlobalColor(attr_color)
                pixmap = QPixmap(50,50)
                pixmap.fill(attr_color)
                attr_icon = QIcon(pixmap)

                for index in range(self.topLevelItemCount()):
                    if self.topLevelItem(index).text(1) == attr_class:
                        self.topLevelItem(index).addChild(QTreeWidgetItem(['', attr_class, name, attr_points]))
                        child_index = self.topLevelItem(index).childCount() - 1
                        self.topLevelItem(index).child(child_index).setIcon(0, attr_icon)


    def delete_item(self):
        item = self.currentItem()
        if self.indexOfTopLevelItem(item) != -1:
            self.setCurrentItem(None)
        else:
            name = item.text(2)
            self.deleteFileAttr(name)

    def deleteFileAttr(self, name):
        self.main.file[str(self.index)].attrs.__delitem__(name)
        self.main.file[str(self.index)].attrs[classifier.tasks.COUNT.value] -=  1
        self.updateFileNames(name)

    def updateFileNames(self, deleted_name):
        for name, value in self.main.file[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                if int(name) > int(deleted_name):
                    self.main.file[str(self.index)].attrs.__delitem__(name)
                    name = int(name)
                    name -= 1
                    self.main.file[str(self.index)].attrs[str(name)] = value
        self.main._refresh_tree.emit()


class polygonPalette(QListWidget):
    def __init__(self, main, parent):
        super().__init__(parent=parent)
        self.main = main
        self.parent = parent
        self.setFlow(QListView.LeftToRight)
        self.setMouseTracking(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.fill()
        self.itemClicked.connect(self.adjust_code)

    def fill(self):
        for triple in self.main.codenamecolor:
            pixmap = QPixmap(50,50)
            pixmap.fill(Qt.GlobalColor(triple[2]))
            self.addItem(QListWidgetItem(QIcon(pixmap), str(triple[0])))

    def leaveEvent(self, event):
        self.setCurrentItem(None)

    def adjust_code(self, item):
        self.parent.adjust_code(item)

class viewToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__()

        self.add_actions()

    def add_actions(self):
        self.first = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'go to first image in project')
        self.previous = self.addAction(QIcon('__icons__/previous_tbtn.png'), 'go to previous image in project')
        self.next = self.addAction(QIcon('__icons__/next_tbtn.png'), 'go to next image in project')
        self.last = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'go to last image in project')
        self.add = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'add new image to project')
        self.delete = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'delete image from project')
        self.showall = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'set all polygons in list as selected')
        self.hideall = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'set all polygons in list as deselected')




"""
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
        self.btn_edit_task = QPushButton("edit task")

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
        self.layout.addWidget(self.btn_edit_task)

        self.setLayout(self.layout)

    def parse_description(self, hdf):
        self.name.setText(classifier.hdfs.NAME.value + hdf.attrs[classifier.hdfs.NAME.value])
        self.description.setText(classifier.hdfs.DESCRIPTION.value + hdf.attrs[classifier.hdfs.DESCRIPTION.value])
        self.task_count.setText(classifier.hdfs.TASK_COUNT.value +  str(hdf.attrs[classifier.hdfs.TASK_COUNT.value])) #str?




class view_control(QGroupBox):
    def __init__(self, _show_all, _edit_task, parent=None):
        super().__init__(parent=parent)
        self._show_all = _show_all
        self._edit_task = _edit_task
        #self.create_Palette()
        self.init_ui()
        self.tree = polygon_classes(parent)
        self.layout.addWidget(self.tree)
        

    def init_ui(self):
        
        self.btn_previous = QPushButton("<<")
        self.btn_next = QPushButton(">>")
        self.btn_show_all = QPushButton("show all")
        self.btn_show_all.clicked.connect(self.on_show_all)
        self.btn_hideall = QPushButton("hide all")
        self.btn_hideall.clicked.connect(self.on_hideall)
        self.btn_edit_task = QPushButton("edit task")
        self.btn_edit_task.clicked.connect(self.on_edit_task)
        

        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.btn_previous)
        self.layout.addWidget(self.btn_next)
        self.layout.addWidget(self.btn_show_all)
        self.layout.addWidget(self.btn_hideall)
        self.layout.addWidget(self.btn_edit_task)
        self.layout.addWidget(self.list)
       
        self.setLayout(self.layout)
    
    def on_show_all(self):
        self._show_all.emit(1)

    def on_hideall(self):
        self._show_all.emit(-1)

    def on_edit_task(self):
        self._edit_task.emit(-1)

    

    def create_Palette(self):
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

    def adjust_Palette(self, hdf):
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
    
#class view_control_new(QGroupBox):
"""