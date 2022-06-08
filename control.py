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

class requirements(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWordWrap(True)
        with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/requirements.txt", 'r') as f:
            text = f.read()
        self.setText(text)


class newestDescription(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.parent = parent
        self.setWindowTitle("Введите новое описание проекта:")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.line = QLineEdit()
        self.layout.addWidget(self.line)
        self.line.textChanged.connect(self.parent.updateFileDescription)

class testDescription(QLabel):
    def __init__(self, parent, main):
        super().__init__(parent=parent)
        self.main = main
        self.setMouseTracking(True)
        self.setWordWrap(True)
    
    def updateFileDescription(self, text):
        self.main.file.attrs[classifier.hdfs.DESCRIPTION.value] = text
        self.updateWidgetDescription()
        if not text:
            self.setText("Описание проекта: ")
    
    def updateWidgetDescription(self):
        self.setText("Описание проекта: " + '\n' + self.main.file.attrs[classifier.hdfs.DESCRIPTION.value])

    def mousePressEvent(self, event):
        if self.main.file:
            getdescription = newestDescription(self)
            getdescription.exec_()
            self.main._parse_projects.emit()

    def enterEvent(self, event):
        with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/style/gbox_hover.qss", 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)

    
    def leaveEvent(self, event):
        with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/style/gbox_widget.qss", 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)    

class newAerialAttr(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.parent = parent
        self.setWindowTitle("Введите новое значение параметра:")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.line = QLineEdit()
        self.layout.addWidget(self.line)
        self.line.textChanged.connect(self.parent.updateFileDescription)

class aerialAttr(QLabel):
    def __init__(self, parent, main, line):
        super().__init__(parent=parent)
        self.main = main
        self.line = line
        self.parent = parent
        self.setMouseTracking(True)
        self.setWordWrap(True)
        self.setObjectName("aerial_attr")
    
    def updateFileDescription(self, text):
        if self.line == classifier.aerial.SOURCE.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.SOURCE.value] = text
        elif self.line == classifier.aerial.ALTITUDE.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.ALTITUDE.value] = text
        elif self.line == classifier.aerial.LATITUDE.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.LATITUDE.value] = text
        elif self.line == classifier.aerial.LONGITUDE.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.LONGITUDE.value] = text
        elif self.line == classifier.aerial.SUN.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.SUN.value] = text
        elif self.line == classifier.aerial.SPATIAL.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.SPATIAL.value] = text
        elif self.line == classifier.aerial.SIZE.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.SIZE.value] = text
        elif self.line == classifier.aerial.DATE.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.DATE.value] = text
        elif self.line == classifier.aerial.TIME.value:
            self.main.file[str(self.parent.index)].attrs[classifier.aerial.TIME.value] = text
        self.updateWidgetDescription()
        if not text:
            self.setText("")
    
    def updateWidgetDescription(self):
        if self.line == classifier.aerial.SOURCE.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.SOURCE.value])
        elif self.line == classifier.aerial.ALTITUDE.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.ALTITUDE.value])
        elif self.line == classifier.aerial.LATITUDE.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.LATITUDE.value])
        elif self.line == classifier.aerial.LONGITUDE.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.LONGITUDE.value])
        elif self.line == classifier.aerial.SUN.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.SUN.value])
        elif self.line == classifier.aerial.SPATIAL.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.SPATIAL.value])
        elif self.line == classifier.aerial.SIZE.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.SIZE.value])
        elif self.line == classifier.aerial.DATE.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.DATE.value])
        elif self.line == classifier.aerial.TIME.value:
            self.setText(self.main.file[str(self.parent.index)].attrs[classifier.aerial.TIME.value])

    def mousePressEvent(self, event):
        if self.main.file:
            if self.parent.index != None:
                getdescription = newAerialAttr(self)
                getdescription.exec_()
            #self.main._parse_projects.emit()

    def enterEvent(self, event):
        with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/style/label_aerial_hover.qss", 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)

    
    def leaveEvent(self, event):
        with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/style/label_aerial.qss", 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)    

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
        self.setObjectName('project_control_box')

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
        #self.layout.addWidget(self.add)
        self.layout.addWidget(self.based)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.requirements)

    def init_content(self):
        self.new = QPushButton("Создать новый файл проекта")
        self.add = QPushButton("Добавить проект из ...")
        self.based = QPushButton("Создать проект на основе существующего")
        #self.description = editDescription(parent=self, main=self.main)
        self.description = testDescription(parent=self, main=self.main)
        self.description.setText("Описание проекта: ")
        self.description.setObjectName("description_label")
        #self.description.setStyleSheet("QLabel#description_label{text-align:top;}")
        self.requirements = requirements()

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
        self.main = parent
        self.index = None
        
        self.adjust_window()
        self.set_layouts()
        self.init_widgets()
        self.fill_layouts()
    
        #with open("/home/iakhmetev/Документы/8.3_version_3_data_labeling/style/label_solo.qss", 'r') as f:
        #    stylesheet = f.read()
        #self.setStyleSheet(stylesheet)

    def update_aerial(self, index):
        self.index = index
        self.mytitle.setText("Параметры снимка: #" + str(index))
        self.source_l.updateWidgetDescription()
        self.altitude_l.updateWidgetDescription()
        self.latitude_l.updateWidgetDescription()
        self.longitude_l.updateWidgetDescription()
        self.sun_l.updateWidgetDescription()
        self.spatial_l.updateWidgetDescription()
        self.size_l.updateWidgetDescription()
        self.date_l.updateWidgetDescription()
        self.time_l.updateWidgetDescription()

    
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
        #self.save = QPushButton("Сохранить")
        #self.discard = QPushButton("Отменить редактирование")
        

        self.source_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.SOURCE.value)
        self.altitude_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.ALTITUDE.value)
        self.latitude_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.LATITUDE.value)
        self.longitude_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.LONGITUDE.value)
        self.sun_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.SUN.value)
        self.spatial_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.SPATIAL.value)
        self.size_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.SIZE.value)
        self.date_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.DATE.value)
        self.time_l = aerialAttr(parent=self, main=self.main, line=classifier.aerial.TIME.value)

        self.mytitle    = QLabel("Параметры снимка:")
        self.source     = QLabel('Летательный аппарат: ')
        self.altitude   = QLabel('Высота        (км): ')
        self.latitude   = QLabel('Широта        (верхний левый пиксель): ')
        self.longitude  = QLabel('Долгота       (верхний левый пиксель): ')
        self.sun        = QLabel('Азимут солнца: ')
        self.spatial    = QLabel('Разрешение    (метр:пиксель): ')
        self.size       = QLabel('Размер        (ширина:высота): ')
        self.date       = QLabel('Дата: ')
        self.time       = QLabel('Время: ')

        self.mytitle.setObjectName('solo')
        self.source.setObjectName('solo')
        self.altitude.setObjectName('solo')
        self.latitude.setObjectName('solo')
        self.longitude.setObjectName('solo')
        self.sun.setObjectName('solo')
        self.spatial.setObjectName('solo')
        self.size.setObjectName('solo')
        self.date.setObjectName('solo')
        self.time.setObjectName('solo')

    def fill_layouts(self):

        self.left.addWidget(self.source)
        self.left.addWidget(self.altitude)
        self.left.addWidget(self.latitude)
        self.left.addWidget(self.longitude)
        self.left.addWidget(self.sun)
        self.left.addWidget(self.spatial)
        self.left.addWidget(self.size)
        self.left.addWidget(self.date)
        self.left.addWidget(self.time)

        self.right.addWidget(self.source_l)
        self.right.addWidget(self.altitude_l)
        self.right.addWidget(self.latitude_l)
        self.right.addWidget(self.longitude_l)
        self.right.addWidget(self.sun_l)
        self.right.addWidget(self.spatial_l)
        self.right.addWidget(self.size_l)
        self.right.addWidget(self.date_l)
        self.right.addWidget(self.time_l)

        self.layout.addWidget(QLabel("Параметры снимка:"), 0, 0)

        #self.layout.addWidget(self.save, 2, 1)
        #self.layout.addWidget(self.discard, 2, 0)
        self.layout.addWidget(self.mytitle, 0, 0)


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
            if utils.ispoints(name):
            #if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
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
            if utils.ispoints(name):
            #if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
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
        #print(classifier.items.first.value)
        self.first = self.addAction(QIcon(classifier.items.first.value), 'go to first image in project')
        self.previous = self.addAction(QIcon(classifier.items.previous.value), 'go to previous image in project')
        self.next = self.addAction(QIcon(classifier.items.next.value), 'go to next image in project')
        self.last = self.addAction(QIcon(classifier.items.last.value), 'go to last image in project')
        self.showall = self.addAction(QIcon(classifier.items.showall.value), 'set all polygons in list as selected')
        self.hideall = self.addAction(QIcon(classifier.items.hideall.value), 'set all polygons in list as deselected')
        self.add = self.addAction(QIcon(classifier.items.add.value), 'add new image to project')
        self.delete = self.addAction(QIcon(classifier.items.delete.value), 'delete image from project')




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