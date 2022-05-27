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
    def __init__(self, parent, main):
        super().__init__(parent=parent)
        self.main = main
        self.shape = shape.shape()
        self.polygon = None
        self.index = 0
        #self.main.signal_showall.connect(self.show_all)
        #self.main.signal_showall.connect(self.hide_all)

        self.adjust_window()
        self.init_background()

    def adjust_window(self):
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setGeometry(QtCore.QRect(0, 0, 800, 600))


    def init_background(self):
        if self.main.file == None:
            image_as_pixmap = utils.pixmap_default()
            self.background = self.scene.addPixmap(image_as_pixmap)
            self.index_max = 0
        else:
            image_as_pixmap = utils.pixmap_at_index(self.main.file, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
            self.index_max = self.main.file.attrs[classifier.hdfs.TASK_COUNT.value] - 1

    def change_pixmap(self,index):
        if self.main.file:
            self.index += index
            if self.index < 0:
                self.index = 0
            elif self.index > self.index_max:
                self.index = self.index_max
            if self.background:  
                self.scene.removeItem(self.background)
            image_as_pixmap = utils.pixmap_at_index(self.main.file, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)

    def set_pixmap(self, index):
        if self.background:  
            self.scene.removeItem(self.background)
        image_as_pixmap = utils.pixmap_at_index(self.main.file, index)
        self.background = self.scene.addPixmap(image_as_pixmap)


    def current_task(self):
        return self.index

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.scale(1.5, 1.5)
        elif event.key() == Qt.Key_Minus:
            self.scale(0.5, 0.5)

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
                print(event.button())
                self.shape.add_point(point)
            elif event.button() == Qt.RightButton and self.point_status:
                self.shape.del_point(self.point_index)
            self.polygon = self.scene.addPolygon(QPolygonF(self.shape.points))
        self.point_status = None
        self.point_index = None

    def mouseMoveEvent(self, event):
        point = self.mapToScene(QPoint(event.x(), event.y()))
        if self.point_index != None:
            if self.point_status:  
                self.scene.removeItem(self.polygon)
                self.shape.change_point(self.point_index, point)
                self.polygon = self.scene.addPolygon(QPolygonF(self.shape.points))

    """
    @pyqtSlot(int)
    def show_all(self, code):
        print("view showall", code)
        if code >= 0:
            if self.main.file:
                color_index = 2
                for name, value in self.main.file[str(self.index)].attrs.items():
                    #print(name, value)
                    
                    if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                        #print(name, value)
                        classes = []
                        a_class = utils.attrs_get_class(value)
                        a_type = utils.attrs_get_type(value)
                        a_points = utils.attrs_get_points(value)
                        for p_class in self.main.file.attrs[classifier.hdfs.CLASSES.value]:
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
                    
    """
    """
    @pyqtSlot(int)
    def hide_all(self, code):
        if code == -1:
            for item in self.scene.items():
                self.scene.removeItem(item)
            image_as_pixmap = utils.pixmap_at_index(self.main.file, self.index)
            self.background = self.scene.addPixmap(image_as_pixmap)
    """


    
class view_view(base_view):
    def __init__(self, parent, main):
        super().__init__(main=main, parent=parent)


class view_edit(base_view):
    def __init__(self, parent, main, current_task=0):
        super().__init__(main=main, parent=parent)

        self.index = current_task
        self.shape_items = []
        self.init_ui()
    
    def init_ui(self):
        self.set_pixmap(self.index)
        self.color_class()
        self.init_widgets()
        self.refresh_attrlist()
        self.connect_ui()
        
    def init_widgets(self):
        self.attr_list = QListWidget()
        self.attr_list.setMinimumSize(200, 200)
        self.attr_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.pallete = QListWidget()
        self.pallete.setSelectionMode(QAbstractItemView.SingleSelection)
        self.adjust_pallete()

    def connect_ui(self):
        #self.attr_list.itemActivated.connect(self.show_shape)
        #self.attr_list.currentItemChanged.connect(self.show_shape)
        self.attr_list.itemSelectionChanged.connect(self.add_attrview)
        self.attr_list.itemDoubleClicked.connect(self.edit_attr)

        self.pallete.itemClicked.connect(self.update_class)


    def refresh_attrlist(self):
        self.attr_list.clear()
        for name, value in self.main.file[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                self.attr_list.addItem(value)

    def delete_attrlistitem(self):
        item = self.attr_list.currentItem()
        for name, value in self.main.file[str(self.index)].attrs.items():
            if item.text() == value:
                self.delete_attrhdf(name)
        #self.attr_list.removeItemWidget(item)
        #self.refresh_attrlist() #без комента не удаляется полигон, с коментом не удаляется строка в списке почему

    def delete_attrhdf(self, attr_name):
        self.main.file[str(self.index)].attrs.__delitem__(attr_name)
        self.main.file[str(self.index)].attrs[classifier.tasks.COUNT.value] -=  1
        for name, value in self.main.file[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                if int(name) > int(attr_name):
                    self.main.file[str(self.index)].attrs.__delitem__(name)
                    name = int(name)
                    name -= 1
                    self.main.file[str(self.index)].attrs[str(name)] = value


    def edit_attr(self, attr):
        #attr = self.attr_list.currentItem()
        self.clear_shape()
        self.clear_scene()
        #self.clear_scene2()
        text = attr.text()
        attr_name = None
        for name, value in self.main.file[str(self.index)].attrs.items():
            if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
                if value == text:
                    attr_name = name
        
        points = utils.attrs_get_points(attr.text())
        points = utils.pointslist_from_str(points)
        points = utils.flist_from_pointslist(points)
        points = utils.qpoints_from_flist(points)
        self.shape.set_points(points)
        self.shape.type = classifier.shapes.POLYGON
        #print(self.polygon)
        #self.polygon = self.scene.addPolygon(self.shape.polygon())
        self.polygon = self.scene.addPolygon(QPolygonF(self.shape.points))
        #self.scene.addPolygon(QPolygonF(self.shape.points))
        #print(self.polygon)
        self.delete_attrhdf(attr_name) ##?????
        self.delete_attrlistitem()
        #self.updateScene()



    def save_attrhdf(self):
        name = self.main.file[str(self.index)].attrs[classifier.tasks.COUNT.value]
        points = utils.flist_from_pointslist(self.shape.points)
        s_type = self.shape.type
        cclass = '000'#message._class.text()
        self.main.file[str(self.index)].attrs[str(name)] = str(s_type) + ';' + cclass + ';' + str(points)
        self.main.file[str(self.index)].attrs[classifier.tasks.COUNT.value] +=  1

        self.scene.removeItem(self.polygon)
        self.shape.clear()
        self.polygon = None
        self.refresh_attrlist()

    def update_class(self, pallete_item):
        if self.attr_list.currentItem():
            for item in self.attr_list.selectedItems():
                text = item.text()
                attr_name = None
                for name, value in self.main.file[str(self.index)].attrs.items():
                    if text == value:
                        attr_name = name
                text = re.sub(r';[0-9][0-9][0-9];', ';' + pallete_item.text() + ';', text)
                self.main.file[str(self.index)].attrs[attr_name] = text
            self.refresh_attrlist()
            self.deselect_class()


    def deselect_class(self):
        self.pallete.setCurrentItem(None)
    
    def deselect_attr(self):
        self.attr_list.setCurrentItem(None)

    def clear_shape(self):
        self.shape.clear()
    
    def clear_scene(self):
        for item in self.scene.items():
            if item.type() != 7:  #7 for pixmap
                self.scene.removeItem(item)

    def clear_scene2(self):
        for item in self.shape_items:
            self.scene.removeItem(item)

    def add_polygon(self):
        self.shape.points.clear()
        self.shape.type = classifier.shapes.POLYGON

    def add_attrview(self):
        self.clear_scene()
        for item in self.attr_list.selectedItems():
            #points = [QPointF(1.0, 2.0), QPointF(2.0, 3.0), QPointF(3.0, 4.0)]
            points = utils.attrs_get_points(item.text())
            points = utils.pointslist_from_str(points)
            points = utils.flist_from_pointslist(points)
            points = utils.qpoints_from_flist(points)
            #print(points)
            #self.scene.addPolygon(QPolygonF(points))
            cclass = utils.attrs_get_class(item.text())
            color = self.get_color_class(cclass)
            #print(color)
            if color:
                brush = QBrush(color, Qt.SolidPattern)
                pen = QPen()
                polygon = self.scene.addPolygon(QPolygonF(points), pen, brush)
                #self.shape_items.append(polygon)

        

    #def save_attr_class(self):




    
    def color_class(self):
        color_index = 2
        self.color_class = []
        for cclass in self.main.file.attrs[classifier.hdfs.CLASSES.value]:
            color = QColor(Qt.GlobalColor(color_index))
            pair = (cclass, color)
            self.color_class.append(pair)
            color_index += 1
            if color_index == 19:
                color_index = 2

    def get_color_class(self, class_index):
        for cclass, color in self.color_class:
            #print(cclass, color, class_index)
            if cclass == class_index:
                return color



    def adjust_pallete(self):
        for cclass, color in self.color_class:
            pixmap = QPixmap(50,50)
            pixmap.fill(color)
            self.pallete.addItem(QListWidgetItem(QIcon(pixmap), cclass))


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
