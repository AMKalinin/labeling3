from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF, pyqtSlot#, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar, QGraphicsView, QGraphicsScene)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon, QPolygonF
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
            self.signal.connect(self.hide_all)

        self.setGeometry(QtCore.QRect(10, 40, 601, 411))
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        if self.hdf == None:
            image_as_pixmap = utils.pixmap_default()
            self.background = self.scene.addPixmap(image_as_pixmap)
    
    @pyqtSlot(int)
    def show_all(self, code):
        if code >= 0:
            if self.hdf:
                color_index = 2
                for name, value in self.hdf[str(self.index)].attrs.items():
                    if value[0]== str(2):
                        #print(name, value)
                        classes = []
                        a_class = utils.attrs_get_class(value)
                        a_type = utils.attrs_get_type(value)
                        a_points = utils.attrs_get_points(value)
                        for clas in self.hdf.attrs[classifier.HDF_FILE_CLASSES]:
                            classes.append(clas[0:3])
                        if str(a_class) in classes:
                            color = QColor(Qt.GlobalColor(color_index))
                            color_index += 1
                            pen = QPen()
                            brush = QBrush(color, Qt.SolidPattern)
                            if a_type == 'Polygon':
                                polygon = QPolygonF()
                                tmp_str2 = re.sub(r' ', '', a_points)
                                tmp_list = re.findall(r'\([0-9]+,[0-9]+\)', tmp_str2)
                                tuple_list = []
                                for pair in tmp_list:
                                    tuple_list.append(make_tuple(pair))
                                for int_pair in tuple_list:
                                    polygon.append(QPoint(int_pair[0], int_pair[1]))
                                self.scene.addPolygon(polygon, pen, brush)
    

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.zoom_in()
        elif event.key() == Qt.Key_Minus:
            self.zoom_out()

    def mousePressEvent(self, event):
        print(event.pos())
        
    def zoom_in(self):
        self.scale(1.5, 1.5)
    
    def zoom_out(self):
        self.scale(0.5, 0.5)

    @pyqtSlot(int)
    def hide_all(self, code):
        if code == -1:
            for item in self.scene.items():
                self.scene.removeItem(item)
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)

    def change_pixmap(self,index):
        if self.hdf:
            self.index += index
            if self.index < 0:
                self.index = 0
            elif self.index > self.index_max:
                self.index = self.index_max
            if self.background:  
                self.scene.removeItem(self.background)
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
    
class view_view(base_view):
    def __init__(self, parent, file_link=None, signal=None):
        super().__init__(parent=parent, file_link=file_link, signal=signal)

        if self.hdf:
            self.index_max = self.hdf.attrs[classifier.HDF_FILE_TASK_COUNT] - 1
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
            self.change_pixmap(self.index)


class view_edit(base_view):
    def __init__(self, parent, file_link=None):
        super().__init__(parent=parent, file_link=file_link)

    

        #for i in range(8):
            #self.hdf[str(0)].attrs[str(i)].__delitem__()
            #self.hdf[str(0)].attrs[str(1)] = "461;Ellipse;[(0,0),(1,1)]"
            #self.hdf[str(0)].attrs[str(2)] = "462;Rect;[(0,0),(1,1)]"
            #self.hdf[str(0)].attrs[str(0)] = "200;Polygon;[(0,0),(100,0), (100,100), (0, 100)]"
            #self.hdf[str(0)].attrs[str(1)] = "210;Polygon;[(100,0),(200,0), (200,100), (100, 100)]"
            #self.hdf[str(0)].attrs[str(2)] = "230;Polygon;[(200,0),(300,0), (300,100), (200, 100)]"