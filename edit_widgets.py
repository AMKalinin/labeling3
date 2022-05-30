from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon, QPolygonF
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene, QMenuBar, QToolBar)
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

class edit_widget_new(QDialog):
    #signal_refreshTree = pyqtSignal()
    def __init__(self, parent, main, index):
        super().__init__(parent=parent)
        self.main = main
        self.index = index

        self.init_ui()


    def init_ui(self):
        self.adjust_window()
        self.init_widgets()
        self.fill_layout()
        self.connect_ui()

    def adjust_window(self):
        size = QSize(1366, 768)
        self.setMinimumSize(size)
        self.setWindowTitle("Окно редактирования полигонов")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def init_widgets(self):
        self.view = view_widgets.view_edit_new(parent=self, main=self.main, current_task=self.index)
        self.tree = control_widgets.polygonTree(parent=self, main=self.main)
        self.tree.update(self.index)
        self.pallete = control_widgets.polygonPallete(parent=self, main=self.main)
        self.toolbar = QToolBar()
        self.add_actions()

    def add_actions(self):
        self.new_polygon = self.toolbar.addAction(QIcon('__icons__/cancel_tbtn.png'), 'go to first image in project')
        self.save = self.toolbar.addAction(QIcon('__icons__/cancel_tbtn.png'), 'go to last image in project')
        self.discard = self.toolbar.addAction(QIcon('__icons__/previous_tbtn.png'), 'go to previous image in project')
        self.delete = self.toolbar.addAction(QIcon('__icons__/next_tbtn.png'), 'go to next image in project')

        #self.add = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'add new image to project')
        #self.delete = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'delete image from project')
        #self.showall = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'set all polygons in list as selected')
        #self.hideall = self.addAction(QIcon('__icons__/cancel_tbtn.png'), 'set all polygons in list as deselected')


    def fill_layout(self):
        self.layout.addWidget(self.toolbar, 0, 0)
        self.layout.addWidget(self.view, 1, 0)
        self.layout.addWidget(self.tree, 1, 1)
        self.layout.addWidget(self.pallete, 2, 0)

    def connect_ui(self):
        self.new_polygon.triggered.connect(self.view.newshape_polygon)
        self.save.triggered.connect(self.view.save_shape)
        self.discard.triggered.connect(self.view.discard)
        self.delete.triggered.connect(self.tree.delete_item)
        self.main.signal_refreshTree.connect(self.tree.fill)
        self.tree.itemDoubleClicked.connect(self.adjust_points)
        #self.signal_adjustCode.connect(self.adjust_code)

    def adjust_code(self, palleteItem):
        #selected = self.tree.currentItem()
        #if selected:
            for item in self.tree.selectedItems():
                if self.tree.indexOfTopLevelItem(item) == -1:
                    attr_index = item.text(2)
                    self.main.adjust_code(self.index, attr_index, palleteItem.text())
            self.main.signal_refreshTree.emit()

    def adjust_points(self, treeItem):
        points = treeItem.text(3)
        points = utils.pointslist_from_str(points)
        points = utils.flist_from_pointslist(points)
        points = utils.qpoints_from_flist(points)

        #s_type = sdfsdfwe
        #self.view.shape_frompoints(points, type)
        #print(points, type(points))
        self.tree.delete_item()
        self.view.discard()
        self.view.shape_frompoints(points)
        #self.view.shape.set_points(points)
        #self.view.shape.set_type(classifier.shapes.POLYGON.value)
        #self.view.polygon = self.view.scene.addPolygon(QPolygonF(self.view.shape.points))




class edit_widget(QDialog):
    signal_parsepolygons = pyqtSignal()
    def __init__(self, main, index, hdf):
        super().__init__()
        self.main = main
        self.index = index
        self.hdf = hdf
        
        self.init_widgets()
        self.init_layout()
        self.connect_ui()
        #self.polygon_list()

    def init_layout(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
    
        self.layout.addWidget(self.edit, 0, 0)
        #self.layout.addWidget(self.showall, 0, 1)
        #self.layout.addWidget(self.hideall, 0, 2)
        #self.layout.addWidget(self.combo, 0, 3)

        self.layout.addWidget(self.polygon, 0, 4)
        #self.layout.addWidget(self.new_item, 1, 4)
        #self.layout.addWidget(self.discard_shape, 2, 4)

        #self.layout.addWidget(self.none, 0, 5)
        self.layout.addWidget(self.edit.attr_list, 0, 6)

        self.layout.addWidget(self.save, 0, 7)
        self.layout.addWidget(self.delete, 2, 7)
        #self.layout.addWidget(self.edit_points, 1, 7)
        #self.layout.addWidget(self.edit_class, 3, 7)

        self.layout.addWidget(self.edit.pallete, 0, 9)


        

    def init_widgets(self):
        self.edit = view_widgets.view_edit(parent=None, main=self.main, current_task=self.index)
        #self.showall = QPushButton("showall")
        #self.hideall = QPushButton("hideall")
        self.polygon = QPushButton("new polygon")
        self.new_item = QPushButton("new item")
        self.discard_shape = QPushButton("discard_shape")
        self.none = QPushButton("none")
        #self.attr_list = QListWidget()
        self.save = QPushButton("save")
        self.delete = QPushButton("delete")
        #self.list = QListWidget()
        self.edit_points = QPushButton("edit points")
        self.edit_class = QPushButton("edit class")

        """
        self.combo = QComboBox()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.combo.addItem(value)
        """
    def connect_ui(self):
        #self.showall.clicked.connect(self.edit.show)
        #self.hideall.clicked.connect(self.edit.hide)
        self.polygon.clicked.connect(self.edit.add_polygon)
        self.none.clicked.connect(self.edit.add_none)
        self.save.clicked.connect(self.edit.save_attrhdf)
        #self.signal_parsepolygons.connect(self.polygon_list)
        self.delete.clicked.connect(self.edit.delete_attrlistitem)
        self.edit_points.clicked.connect(self.edit.edit_attr)

    """
    def polygon_list(self):
        #print("parsed")
        #if self.attr_list:
        #    self.attr_list.deleteLater()
        self.attr_list.clear()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.attr_list.addItem(value)
    """

