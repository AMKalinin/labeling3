from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF#, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar, QGraphicsView, QGraphicsScene, QTreeWidgetItem)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5 import QtWidgets, QtGui, QtCore
import os
import h5py
import numpy as np
import cv2
import classifier
#import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple
from PyQt5.QtCore import pyqtSignal, QObject

def pixmap_default():
    return QPixmap("img_default.jpg")

def attrs_get_type(attrs):
    return attrs.split(';')[0]

def attrs_get_class(attrs):
    return attrs.split(';')[1]

def attrs_get_points(attrs):
    return attrs.split(';')[2]

def give_points(attrs_points):
    rtn = []
    xy = re.search(r'[0-9]*\.[0-9]*, [0-9]*\.[0-9]*', xy).group(0)
    xy = xy.split(',')
    x = float(xy[0])
    y = float(xy[1])
    return rtn
    #print(attrs_points)


def pixmap_at_index(file_link, index):

    hdf = file_link
    myindex = str(index)
    dataset = hdf[str(index)]
    image_as_numpy = dataset[()]
    height, width, channel = image_as_numpy.shape
    bytesPerLine = 3 * width
    image_as_qimage = QImage(image_as_numpy, width, height, bytesPerLine, QImage.Format_RGB888)
    image_correct_rgb = image_as_qimage.rgbSwapped()
    image_as_pixmap = QPixmap(image_correct_rgb)
    return image_as_pixmap

def clear_layout(layout):
    for i in reversed(range(layout.count())): 
        layout.itemAt(i).widget().deleteLater()
        
def check_create_projects_folder():
    if not os.path.exists(classifier.items.PROJECTS.value):
        os.mkdir(classifier.items.PROJECTS.value)

def fill_tree(tree):
    bases = [(x, y) for x, y in zip(classifier.bases.unique_id(), classifier.bases.name())]
    classes = [(x, y, z) for x,y,z in zip(classifier.classes.base(), classifier.classes.code(), classifier.classes.name())]
    for base in bases:
        tmp = QTreeWidgetItem([base[1]])
        tree.addTopLevelItem(tmp)
        for item in classes:
            if item[0] == base[0]:
                child = QTreeWidgetItem([item[2], str(item[1])])
                tmp.addChild(child)

def pointslist_from_str(str):
    rtn = []
    points = re.findall(r'([0-9]*\.[0-9]*, [0-9]*\.[0-9]*)', str)
    #print(points)
    return points

def flist_from_pointslist(list):
    rtn = []
    for point in list:
        xy = str(point)
        xy = re.search(r'[0-9]*\.[0-9]*, [0-9]*\.[0-9]*', xy).group(0)
        xy = xy.split(',')
        x = float(xy[0])
        y = float(xy[1])
        xy = (x, y)
        rtn.append(xy)
    return rtn

def qpoints_from_flist(list):
    rtn = []
    for point in list:
        rtn.append(QPointF(point[0], point[1]))
    return rtn

def str_from_flist(list):
    print('\n'.join([str(x) for t in list for x in t]))


def points_from_x_y(list):
    pass

def get_name(path):
    name = re.search(r'[/][^/]*\.hdf', path).group(0)
    return name[1:-4]

def get_description(path):
    with h5py.File(path, 'r') as hdf:
        description = hdf.attrs[classifier.hdfs.DESCRIPTION.value]
    return description

def get_alltasks(path):
    with h5py.File(path, 'r') as hdf:
        alltasks = hdf.attrs[classifier.hdfs.TASK_COUNT.value]
    return alltasks

def get_donetasks(path):
    donetasks = 0
    with h5py.File(path, 'r') as hdf:
        max_index = hdf.attrs[classifier.hdfs.TASK_COUNT.value]
        for index in range(max_index):
            if hdf[str(index)].attrs[classifier.tasks.STATUS.value] == classifier.tasks.DONE.value:
                donetasks += 1
    return donetasks

def get_startdate(path):
    startdate = os.path.getctime(path)
    return startdate

def get_lastupdate(path):
    lastupdate = os.path.getmtime(path)
    return lastupdate

"""
def update_attrs_names(hdf, name):
    #if open
    for name, value in self.hdf[str(self.index)].attrs.items():

    def delete_attrs(self):
        for item in self.p_list.selectedItems():
            for name, value in self.hdf[str(self.index)].attrs.items():
                if item.text() == value:
                    self.hdf[str(self.index)].attrs.__delitem__(name)
                    self.hdf[str(self.index)].attrs[classifier.tasks.COUNT.value] -=  1
        self.refresh_attrs()
"""