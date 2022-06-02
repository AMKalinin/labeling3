from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtCore import Qt, QRect, QPoint, QPointF

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QRect #, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon, QPolygonF



import os
import h5py
import numpy as np
import cv2
import classifier

import re
from ast import literal_eval as make_tuple


class shape():
    tell_apart_distance = 3
    def __init__(self, points=None):
        #self.tell_apart_distance = 3
        self.type = classifier.shapes.NONE.value
        #self.code = None
        if points==None:
            self.points = []
        else:
            self.points = points

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

    def closest_to(self, point2):
        if self.points:
            closest_point = self.points[0]
            minimal_distance = self.distance(closest_point, point2)
            for point in self.points:
                distance = self.distance(point, point2)
                if distance < minimal_distance:
                    minimal_distance = distance
                    closest_point = point
            return closest_point

    def index_of(self, point):
        return self.points.index(self.closest_to(point))

    def add_point(self, pos):
        if not self.points:
            self.points.append(QPointF(pos.x(), pos.y()))
        else:
            if not self.point_at_pos(pos):
                closest_index = self.points.index(self.closest_to(pos)) 
                self.points.insert(closest_index, QPointF(pos.x(), pos.y()))

    def delete_point(self, index):
        if self.points:
            self.points.pop(index)

    def change_point(self, index, newpoint):
        self.points[index] = newpoint

    def polygon(self):
        return QPolygonF(self.points)

    def clear(self):
        self.points.clear()
        #self.code = None
        self.type = classifier.shapes.NONE.value

    def set_points(self, points):
        self.points = points

    def set_type(self, s_type):
        self.type = s_type

    def set_shape(self, s_type, points):
        self.set_points(points)
        self.set_type(s_type)

