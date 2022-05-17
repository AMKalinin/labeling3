from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF, pyqtSlot, QItemSelectionModel#, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar, QGraphicsView, QGraphicsScene, QMessageBox, QListWidget, QListWidgetItem,QAbstractItemView)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon, QPolygonF
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import h5py
import numpy as np
import cv2
import classifier
#import segflex_draw_window as draw
import shape
import re
from ast import literal_eval as make_tuple
from PyQt5.QtCore import pyqtSignal, QObject
import utils
import time

class base_view(QGraphicsView):
    def __init__(self, parent, file_link=None, signal=None):
        super().__init__(parent=parent)
        self.shape = shape.shape()
        self.polygon = None
        self.hdf = file_link
        self.index = 0
        self.index_max = 0
        self.signal_showall = signal
        if self.signal_showall:
            self.signal_showall.connect(self.show_all)
            self.signal_showall.connect(self.hide_all)

        self.setGeometry(QtCore.QRect(10, 40, 601, 411))
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        if self.hdf == None:
            image_as_pixmap = utils.pixmap_default()
            self.background = self.scene.addPixmap(image_as_pixmap)
        else:
            self.index_max = self.hdf.attrs[classifier.hdfs.TASK_COUNT.value] - 1
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)

    def current_task(self):
        return self.index


    @pyqtSlot(int)
    def show_all(self, code):
        print("view showall", code)
        if code >= 0:
            if self.hdf:
                color_index = 2
                for name, value in self.hdf[str(self.index)].attrs.items():
                    #print(name, value)
                    
                    if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                        #print(name, value)
                        classes = []
                        a_class = utils.attrs_get_class(value)
                        a_type = utils.attrs_get_type(value)
                        a_points = utils.attrs_get_points(value)
                        for p_class in self.hdf.attrs[classifier.hdfs.CLASSES.value]:
                            classes.append(p_class[0:3])
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
        point = self.mapToScene(QPoint(event.x(), event.y()))
        self.point_index = None
        self.point_status = self.shape.point_at_pos(point)
        if self.point_status: 
            self.point_index = self.shape.index_of_closest(point)


    def mouseReleaseEvent(self, event):
        point = self.mapToScene(QPoint(event.x(), event.y()))
        if self.polygon:
            self.scene.removeItem(self.polygon)
        if self.shape.type == classifier.shapes.POLYGON:
            point = self.mapToScene(QPoint(event.x(), event.y()))
            if event.button() == Qt.LeftButton:
                self.shape.add_point(point)
            elif event.button() == Qt.RightButton and self.point_status:
                self.shape.del_point(self.point_index)
            self.polygon = self.scene.addPolygon(QPolygonF(self.shape.points))
        self.point_status = None
        self.point_index = None

    def mouseMoveEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = self.mapToScene(QPoint(event.x(), event.y()))
            if self.point_index != None:
                if self.point_status:  
                    self.scene.removeItem(self.polygon)
                    self.shape.change_point(self.point_index, point)
                    self.polygon = self.scene.addPolygon(QPolygonF(self.shape.points))



        
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

    def set_pixmap(self, index):
        if self.background:  
            self.scene.removeItem(self.background)
        image_as_pixmap = utils.pixmap_at_index(self.hdf, index)
        self.background = self.scene.addPixmap(image_as_pixmap)

    
class view_view(base_view):
    def __init__(self, parent, file_link=None, signal=None):
        super().__init__(parent=parent, file_link=file_link, signal=signal)
        """
        if self.hdf:
            self.index_max = self.hdf.attrs[classifier.HDF_FILE_TASK_COUNT] - 1
            image_as_pixmap = utils.pixmap_at_index(self.hdf, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
            self.change_pixmap(self.index)
        """

class view_edit(base_view):
    def __init__(self, parent, file_link=None, signal=None, current_task=0, signal_parsepolygons=None):
        super().__init__(parent=parent, file_link=file_link, signal=signal)

        self.set_pixmap(current_task)
        self.index = current_task
        self.signal = signal_parsepolygons
        self.p_list = QListWidget()
        self.p_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.p_list.itemActivated.connect(self.show_shape)
        #self.p_list.currentItemChanged.connect(self.show_shape)
        #self.p_list.itemSelectionChanged.connect(self.show_shape)
        self.p_list.itemDoubleClicked.connect(self.edit_attr)
        self.refresh_attrs()
        self.polygons = []
        self.shapes = []
        self.pallete = QListWidget()
        self.pallete.setSelectionMode(QAbstractItemView.NoSelection)
        self.adjust_pallete()

    def refresh_attrs(self):
        self.p_list.clear()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.p_list.addItem(value)

    def delete_attrs(self):
        for item in self.p_list.selectedItems():
            for name, value in self.hdf[str(self.index)].attrs.items():
                if item.text() == value:
                    self.hdf[str(self.index)].attrs.__delitem__(name)
                    self.hdf[str(self.index)].attrs[classifier.tasks.COUNT.value] -=  1
        self.refresh_attrs()

    def save_attr_new(self):
        shape_number = str(self.hdf[str(self.index)].attrs[classifier.tasks.COUNT.value])
        points = utils.flist_from_pointslist(self.shape.points)
        s_type= self.shape.type
        
        message = QDialog()
        message._class = QLineEdit()
        message.layout = QVBoxLayout()
        message.layout.addWidget(message._class)
        message.setLayout(message.layout)
        message.exec_()

        _class = message._class.text()
        self.hdf[str(self.index)].attrs[str(shape_number)] = str(s_type) + ';' + _class + ';' + str(points)
        self.hdf[str(self.index)].attrs[classifier.tasks.COUNT.value] +=  1
        self.scene.removeItem(self.polygon)
        self.shape.clear()
        self.polygon = None
        self.refresh_attrs()

    def save_attr_points(self, attr):
        text = attr.text()
        c_class = utils.attrs_get_class(text)
        c_type = utils.attrs_get_type(text)
        points = utils.flist_from_pointslist(self.shape.points)
        for name, value in self.hdf[str(self.index)].attrs.items():
            if text == value:
                attr_name = name
        self.hdf[str(self.index)].attrs[attr_name] = c_type + ';' + c_class + ';' + str(points)
        
    
    def save_attr_class(self, attr):
        text = attr.text()
        c_type = utils.attrs_get_type(text)
        points = utils.attrs_get_points(text)
        c_class = self.pallete.currentItem().text()
        for name, value in self.hdf[str(self.index)].attrs.items():
            if text == value:
                attr_name = name
        self.hdf[str(self.index)].attrs[attr_name] = c_type + ';' + c_class + ';' + str(points)

        

    #def save_attr_class(self):



    def edit_attr(self, attr):
        self.clear_shape()
        self.clear_scene()
        
        points = utils.attrs_get_points(attr.text())
        points = utils.pointslist_from_str(points)
        points = utils.flist_from_pointslist(points)
        points = utils.qpoints_from_flist(points)
        self.shape.set_points(points)
        self.shape.type = classifier.shapes.POLYGON
        self.polygon = self.scene.addPolygon(self.shape.polygon())
        self.delete_attrs()
    
    def clear_shape(self):
        self.shape.clear()
    
    def clear_scene(self):
        for item in self.scene.items():
            if item.type() != 7:  #7 for pixmap
                self.scene.removeItem(item)


    def adjust_pallete(self):
        color_index = 2
        for cclass in self.hdf.attrs[classifier.hdfs.CLASSES.value]:
            pixmap = QPixmap(50,50)
            color = QColor(Qt.GlobalColor(color_index))
            pixmap.fill(color)
            self.pallete.addItem(QListWidgetItem(QIcon(pixmap), cclass))
            color_index += 1
            if color_index == 19:
                color_index = 2



    """
    def edit_shape(self, item):
        points = utils.attrs_get_points(item.text())
        points = utils.pointslist_from_str(points)
        points = utils.flist_from_pointslist(points)
        points = utils.qpoints_from_flist(points)
        for item1 in self.scene.items():
            if item1.type() != 7:  #7 for pixmap
                self.scene.removeItem(item1)

        for name, value in self.hdf[str(self.index)].attrs.items():
            if item.text() == value:
                self.hdf[str(self.index)].attrs.__delitem__(name)

        #self.shape = shape.shape(points)
        #self.add_polygon()
        self.shape = shape.shape(points)
        self.shape.type = classifier.shapes.POLYGON
        self.polygon = self.scene.addPolygon(QPolygonF(points))
    """

    """
    def show_shape(self):
        for item in self.scene.items():
            if item.type() != 7:  #7 for pixmap
                self.scene.removeItem(item)

        for item in self.p_list.selectedItems():
            #points = [QPointF(1.0, 2.0), QPointF(2.0, 3.0), QPointF(3.0, 4.0)]
            points = utils.attrs_get_points(item.text())
            points = utils.pointslist_from_str(points)
            points = utils.flist_from_pointslist(points)
            points = utils.qpoints_from_flist(points)
            #print(points)
            self.scene.addPolygon(QPolygonF(points))
    """

    def add_none(self):
        self.shape.points.clear()
        self.shape.type = classifier.shapes.NONE

    def add_rectangle(self):
        self.shape.points.clear()
        self.shape.type = classifier.shapes.RECTANGLE

    def add_polygon(self):
        self.shape.points.clear()
        self.shape.type = classifier.shapes.POLYGON

    def add_ellipse(self):
        self.shape.points.clear()
        self.shape.type = classifier.shapes.ELLIPSE 
    
    """
    def show(self):
        self.show_all(1)
    
    def hide(self):
        self.hide_all(-1)
    """
