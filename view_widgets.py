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
import classifier
import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple
from PyQt5.QtCore import pyqtSignal, QObject
import utils
import time

class base_view(QGraphicsView):
    def __init__(self, parent, file_link=None, signal=None):
        super().__init__(parent=parent)
        self.hdf = file_link
        self.index = 0
        self.index_max = 0
        self.signal = signal
        if self.signal:
            self.signal.connect(self.show_all)

        self.setGeometry(QtCore.QRect(10, 40, 601, 411))
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        if self.hdf == None:
            image_as_pixmap = utils.pixmap_default()
            self.background = self.scene.addPixmap(image_as_pixmap)

        #self.show_all()
    def get_hdf(self):
        return self.hdf

    @pyqtSlot()
    def show_all(self):
        if self.hdf:
            for name, value in self.hdf[str(self.index)].attrs.items():
                print(name, value)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.zoom_in()
        elif event.key() == Qt.Key_Minus:
            self.zoom_out()
        
    def zoom_in(self):
        self.scale(1.5, 1.5)
    
    def zoom_out(self):
        self.scale(0.5, 0.5)


    def hide_all(self):
        print(self.scene.items())

class view_view(base_view):
    def __init__(self, parent, file_link=None, signal=None):
        super().__init__(parent=parent, file_link=file_link, signal=signal)
        self.hide_all()

        if self.hdf:
            self.index_max = self.hdf.attrs[classifier.HDF_FILE_TASK_COUNT] - 1
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
            self.change_pixmap(self.index)

    def change_pixmap(self,index):
        if self.hdf:
            if self.index < self.index_max and self.index >= 0:
                self.index += index
                if self.index < 0:
                    self.index = 0
            self.scene.removeItem(self.background)
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)

class view_edit(base_view):
    def __init__(self, parent, file_link=None):
        super().__init__(parent=parent, file_link=file_link)

    

