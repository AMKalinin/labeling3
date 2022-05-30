from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon, QPolygonF
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter, QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene, QMenuBar, QToolBar)
from PyQt5 import QtWidgets, QtGui, QtCore

import view
import os
import json
import classifier
import utils
import h5py
import time
import re
import cv2
import control

class editWidget(QDialog):
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
        self.view = view.view_edit_new(parent=self, main=self.main, current_task=self.index)
        self.tree = control.polygonTree(parent=self, main=self.main)
        self.tree.update(self.index)
        self.pallete = control.polygonPallete(parent=self, main=self.main)
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

        self.tree.delete_item()
        self.view.discard()
        self.view.shape_frompoints(points)
