from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QRectF#, QVector
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

def attrs_get_class(attrs):
    return attrs.split(';')[0]

def attrs_get_type(attrs):
    return attrs.split(';')[1]

def attrs_get_points(attrs):
    return attrs.split(';')[2]


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