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
import datetime
import h5py
import numpy as np
import cv2
import classifier
#import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import  QFontDatabase
from qssimport import stylesheet
import pathlib


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

def get_task_polygons(hdf, index):
    count = 0
    for name, value in hdf[str(index)].attrs.items():
        if name != classifier.tasks.COUNT.value and name != classifier.tasks.STATUS.value:
            count += 1
    return count
    
def get_startdate(path):
    startdate = os.path.getctime(path)# getctime for windows only
    return startdate

def get_lastupdate(path):
    lastupdate = os.path.getmtime(path)
    return lastupdate

def create_preview(hdf, identifier): #load froma data???
    dataset = hdf[str(identifier)]
    image_as_numpy = dataset[()]
    height, width, channel = image_as_numpy.shape
    bytesPerLine = 3 * width
    image_as_qimage = QImage(image_as_numpy, width, height, bytesPerLine, QImage.Format_RGB888)
    image_correct_rgb = image_as_qimage.rgbSwapped()
    image_as_pixmap = QPixmap(image_correct_rgb)
    image_resized = image_as_pixmap.scaled(100, 100)
    return image_resized

def create_microimage(path, identifier): #load froma data???
    with h5py.File(path, 'r') as hdf:
        max_index = hdf.attrs[classifier.hdfs.TASK_COUNT.value]
        if identifier < max_index:
            dataset = hdf[str(identifier)]
            image_as_numpy = dataset[()]
            height, width, channel = image_as_numpy.shape
            bytesPerLine = 3 * width
            image_as_qimage = QImage(image_as_numpy, width, height, bytesPerLine, QImage.Format_RGB888)
            image_correct_rgb = image_as_qimage.rgbSwapped()
            image_resized = image_correct_rgb.scaled(25, 25)
        else:
            image_resized = QImage(25, 25, QImage.Format_RGB888)
            #image_resized.fill(Qt.GlobalColor(3))
            image_resized.fill(QColor('#E7E7E9'))
    return image_resized

def fill_tree_with_select_classes(tree, classes_code):
    b_old = [int(x[0])-1 for x in classes_code]
    bases = [(x, y) for x, y in zip(classifier.bases.unique_id(), classifier.bases.name()) if x in b_old]
    cls_old = [int(x) for x in classes_code]
    classes = [(x, y, z) for x, y, z in zip(classifier.classes.base(), classifier.classes.code(), classifier.classes.name()) if y in cls_old]
    for base in bases:
        tmp = QTreeWidgetItem([base[1]])
        tree.addTopLevelItem(tmp)
        for item in classes:
            if item[0] == base[0]:
                child = QTreeWidgetItem([item[2], str(item[1])])
                tmp.addChild(child)

def check_cv2format(name):
    cutted_name = name[-5:]
    extension = re.search(r'\..*', cutted_name).group(0)
    if (extension == '.bmp' or
        extension == '.jpeg' or
        extension == '.jpg' or 
        extension == '.png' or 
        extension == '.tiff' or 
        extension == '.tif'):
        return True
    return False

def load_fonts():
    fonts_path = classifier.items.FONTS.value
    if os.path.exists(fonts_path):
        fonts_list = os.listdir(fonts_path)
        for name in fonts_list:
            full_name = fonts_path + name
            QFontDatabase.addApplicationFont(full_name)

def cut_long_string(string, n):
    if len(string) > n:
        return string[:n] + '...'
    return string

def endline_long_sting(string, n):
    strlen = len(string)
    n_in_string = strlen // n
    newstr = ''
    if strlen > n:
        for i in range(n_in_string):
            cutstr = string[i * n: i * (n + 1)] + '\n'
            newstr += cutstr
    return newstr


def load_style(app):
        #print(dir(stylesheet))
        style = stylesheet.StyleSheet(base_dir='/home/iakhmetev/Документы/8.3_version_3_data_labeling/style',
                                        import_def_file='imports.qss')
                                        #main_stylesheet='myStyle.qss')
        app.setStyleSheet(style.load_stylesheet())
    #with open('style.qss', 'r') as f:
    #    style = f.read()
    #    app.setStyleSheet(style)


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