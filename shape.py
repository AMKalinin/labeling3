from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtCore import Qt, QRect, QPoint, QPointF

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QRect #, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon



import os
import h5py
import numpy as np
import cv2
import classifier

import re
from ast import literal_eval as make_tuple


class shape():
    def __init__(self):
        self.tell_apart_distance = 3
        self.type = classifier.shapes.NONE
        self._class = None
        self.points = []

    def distance(self, point1, point2):
        a = (point1.x() - point2.x()) 
        b = (point1.y() - point2.y()) 
        c = (a ** 2 + b ** 2) ** 0.5
        return c

    def point_at_pos(self, point2):
        for point1 in self.points:
            if self.distance(point1, point2) < self.tell_apart_distance:
                return True
        return False

    def closest_to_pos(self, point2):
        if self.points:
            closest_point = self.points[0]
            minimal_distance = self.distance(closest_point, point2)
            for point in self.points:
                distance = self.distance(point, point2)
                if distance < minimal_distance:
                    minimal_distance = distance
                    closest_point = point
            return closest_point

    def index_of_closest(self, point):
        return self.points.index(self.closest_to_pos(point))

    def add_point(self, pos):
        if not self.points:
            self.points.append(QPointF(pos.x(), pos.y()))
        else:
            if not self.point_at_pos(pos):
                closest_index = self.points.index(self.closest_to_pos(pos)) 
                self.points.insert(closest_index, QPointF(pos.x(), pos.y()))

    def change_point(self, index, newpos):
        self.points[index] = newpos


"""
class mask:
    def __init__(self):
        self.code = None
        self.points = []

    def draw(self, pixmap):
        pass

    def distance(self, pos, ind):
        return ((self.points[ind].x() - pos.x())**2 + (self.points[ind].y() - pos.y())**2)**0.5

    def min_dist(self, pos):
        min_ind = 0
        min_dist = self.distance(pos, 0)
        for i in range(1, len(self.points)):
            dist = self.distance(pos, i)
            if dist < min_dist:
                min_dist = dist
                min_ind = i
        return min_ind, min_dist

    def click_on_point(self, pos):
        ind, dist = self.min_dist(pos)
        return dist <= 10, ind

class polygon_mask(mask):
    def __init__(self):
        super(polygon_mask, self).__init__()
        self.type = '<QPolygon>'
        self.polygon = QPolygon()

    def setPoint(self, ind, point):
        self.points[ind] = point
        self.polygon = QPolygon(self.points)

    def add_points(self, point):
        self.points.append(point)
        self.polygon = QPolygon(self.points)

    def draw(self, pixmap):
        painter = QPainter(pixmap)
        painter.drawPolygon(self.polygon)
        painter.setPen((QPen(Qt.black, 10.0)))
        painter.drawPoints(self.polygon)


class rectangle_mask(mask):

    def __init__(self):
        super(rectangle_mask, self).__init__()
        self.type = '<QRect>'
        self.rect = QRect()

    def rectangle(self, p1, p2):
        self.rect = QRect(p1, p2)
        self.points.clear()
        self.calc_points()

    def calc_points(self):
        self.points.append(self.rect.topLeft())
        self.points.append(self.rect.topRight())
        self.points.append(self.rect.bottomRight())
        self.points.append(self.rect.bottomLeft())

    def setPoint(self, ind, point):
        if ind == 0:
            self.points[0] = point
        elif ind == 1:
            self.points[0] = QPoint(self.points[0].x(), point.y())
            self.points[2] = QPoint(point.x(), self.points[2].y())
        elif ind == 2:
            self.points[2] = point
        elif ind == 3:
            self.points[0] = QPoint(point.x(), self.points[0].y())
            self.points[2] = QPoint(self.points[2].x(), point.y())
        self.rectangle(self.points[0], self.points[2])


    def draw(self, pixmap):
        painter = QPainter(pixmap)
        painter.drawRect(self.rect)
        painter.setPen((QPen(Qt.black, 10.0)))
        polygon = QPolygon(self.points)
        painter.drawPoints(polygon)

class Label(QLabel):
    def __init__(self, parent=None):
        super().__init__()

        self.base_pixmap = QPixmap()
        self.overlayed_pixmap = QPixmap()
        self.new_polygon_pixmap = QPixmap()

        self.polygon_for_iterations = QPolygon()
        self.new_polygon = QPolygon()
        self.new_polygon_points = []

        self.maska = mask.mask()
        self.index = None

        self.mode = 'display base'

    def update_base(self, pixmap):
        self.base_pixmap = pixmap.copy()
        self.overlayed_pixmap = pixmap.copy()
        self.new_polygon_pixmap = pixmap.copy()

        #self.update()

    def overlay_mask(self, polygon):
        self.polygon_for_iterations = polygon

        self.mode = 'display mask'
        self.repaint()

    def restore_srcs(self):
        self.mode = 'display base'
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.mode == 'draw polygon':
                self.index = None
                if not self.maska.points:
                    flag = False
                else:
                    flag, ind = self.maska.click_on_point(event.pos())
                if flag:
                    self.index = ind
                else:
                    self.maska.add_points(event.pos())
                    self.update()
                    self.update_base(self.base_pixmap)

            elif self.mode == 'draw rect':
                self.index = None
                if not self.maska.points:
                    flag = False
                else:
                    flag, ind = self.maska.click_on_point(event.pos())
                if flag:
                    self.index = ind
                else:
                    self.start_p = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.mode == 'draw polygon':
                if self.index is not None:
                    self.maska.setPoint(self.index, event.pos())
                    self.update()
                    self.update_base(self.base_pixmap)

            elif self.mode == 'draw rect':
                if self.index is not None:
                    self.maska.setPoint(self.index, event.pos())
                    self.update()
                    self.update_base(self.base_pixmap)
                else:
                    self.maska.rectangle(self.start_p, event.pos())
                    self.update()
                    self.update_base(self.base_pixmap)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(1))
        pixmap = QPixmap()
        if self.mode == 'display base':
            pixmap = self.base_pixmap
        elif self.mode == 'display mask':
            pixmap = self.overlayed_pixmap
            painter2 = QPainter(pixmap)
            painter2.drawPolygon(self.polygon_for_iterations)
            self.overlayed_pixmap = pixmap
            self.toggle_show_hide_mask = False
        elif (self.mode == 'draw polygon') or (self.mode == 'move point') or (self.mode == 'draw rect'):
            pixmap = self.new_polygon_pixmap
            self.maska.draw(pixmap)
        painter.drawPixmap(0, 0, pixmap)

    def select_lable(self):
        self.lable_dialog = dialog(self)
        self.lable_dialog.exec_()
"""