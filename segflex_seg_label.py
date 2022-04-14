from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QRectF, pyqtSlot#, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar, QGraphicsView, QGraphicsScene)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier
import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple
from PyQt5.QtCore import pyqtSignal, QObject
import utils
import time

class view_project(QGraphicsView):
    def __init__(self, parent, file_link=None):
        super().__init__(parent = parent)

        self.index = 0
        self.index_max = 0
        self.hdf = file_link
        self.setGeometry(QtCore.QRect(10, 40, 601, 411))
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        if file_link == None:
            image_as_pixmap = utils.pixmap_default()
            self.background = self.scene.addPixmap(image_as_pixmap)
        else:
            self.index_max = self.hdf.attrs[classifier.HDF_FILE_TASK_COUNT] - 1
            #assert no images in file
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
            self.change_pixmap(0)

    def change_pixmap(self,index):
        if self.hdf:
            if self.index < self.index_max and self.index >= 0:
                self.index += index
                if self.index < 0:
                    self.index = 0
            self.scene.removeItem(self.background)
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
            
