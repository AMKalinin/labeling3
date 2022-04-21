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
        ltx = 0
        lty = 0
        rtx = 10
        rty = 0
        brx = 10
        bry = 10
        for i in range(100):
            color = QColor(Qt.GlobalColor(i))
            pen = QPen()
            brush = QBrush(color, Qt.SolidPattern)
            polygon = QPolygonF(QRectF(QPointF(ltx, lty), QPointF(brx, bry)))
            self.scene.addPolygon(polygon, pen, brush)
            ltx += 10
            brx += 10



    """
    @pyqtSlot()
    def show_all(self):
        if self.hdf:
            
            for name, value in self.hdf[str(self.index)].attrs.items():
                print(name, value)
            
                if value[0]== str(4):
                #try:
                    #print(name, value)
                    print("####################################")
                    #print(utils.attrs_get_class(value))
                    a_class = utils.attrs_get_class(value)
                    a_type = utils.attrs_get_type(value)
                    a_points = utils.attrs_get_points(value)
                    rgb_r = int(a_class[0]) * 20 
                    rgb_g = int(a_class[1]) * 20 
                    rgb_b = int(a_class[2]) * 20 
                    #print("pen=", rgb_r, rgb_g, rgb_b)
                    #print(a_type == 'Polygon')
                    print("color = ", type(Qt.GlobalColor))
                    color = QColor(Qt.GlobalColor(29))
                    #color = QColor(rgb_r,rgb_g,rgb_b, 150)
                    #color = QColor(100,100,100,100)
                    print(color.alphaF())
                    #print("1")
                    #brush = QBrush(color, Qt.Dense2Pattern)
                    #print("2")
                    #pen = QPen(brush)
                    pen = QPen()
                    #print("3")
                    brush = QBrush(color, Qt.SolidPattern)
                    
                    if a_type == 'Polygon':
                        print("---------")
                        polygon = QPolygonF()
                        #tmp_str1 = image_srcs.attrs[str(index)]
                        print(a_points)
                        tmp_str2 = re.sub(r' ', '', a_points)
                        print(tmp_str2)
                        tmp_list = re.findall(r'\([0-9]+,[0-9]+\)', tmp_str2)
                        print("list", tmp_list)
                        tuple_list = []
                        
                        for pair in tmp_list:
                            tuple_list.append(make_tuple(pair))
                        for int_pair in tuple_list:
                            print(int_pair[0], int_pair[1])
                            polygon.append(QPoint(int_pair[0], int_pair[1]))
                        #print(polygon)
                        self.scene.addPolygon(polygon, pen, brush)#pen, brush)
                        print("+++++++")
                        #print(self.scene.items())

                    #print(utils.attrs_get_type(value))
                    #print(utils.attrs_get_points(value))
                #except: 
                #    pass
            
            #self.hdf[str(0)].attrs[str(0)] = "460;Polygon;[(0,0),(1,1)]"
            #self.hdf[str(0)].attrs[str(1)] = "461;Ellipse;[(0,0),(1,1)]"
            #self.hdf[str(0)].attrs[str(2)] = "462;Rect;[(0,0),(1,1)]"
            #self.hdf[str(0)].attrs[str(5)] = "464;Polygon;[(100,0),(200,0), (200,100), (100, 100)]"
            #self.hdf[str(0)].attrs[str(7)] = "364;Polygon;[(200,0),(300,0), (300,100), (200, 100)]"
    """            

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

    

