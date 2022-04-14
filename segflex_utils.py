from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QRectF#, QVector
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
import segflex_classifier as classifier
import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple
from PyQt5.QtCore import pyqtSignal, QObject

def pixmap_default():
    return QPixmap("img_default.jpg")


def pixmap_at_index(file_link, index):

    hdf = file_link
    myindex = str(index)
    #group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
    print(myindex)
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