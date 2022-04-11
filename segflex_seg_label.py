from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QRectF, pyqtSlot#, QVector
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
import segflex_utils as utils
import time

"""
class Label(QLabel):
    def __init__(self, parent=None):
        super().__init__()

        self.base_pixmap = QPixmap()
        self.overlayed_pixmap = QPixmap()
        self.new_polygon_pixmap = QPixmap()

        self.polygon_for_iterations = QPolygon()
        self.new_polygon = QPolygon()
        self.new_polygon_points = []

        self.scroll = QScrollArea()
        self.scroll.setWidget(self)
        self.scroll.setWidgetResizable(True)
        #self.scroll.setFrameShape(QFrame.NoFrame)

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
                self.new_polygon_points.append(event.pos())
                #self.new_polygon = QPolygon(self.new_polygon_points)
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
        elif self.mode == 'draw polygon':
            pixmap = self.new_polygon_pixmap
            self.new_polygon = QPolygon(self.new_polygon_points)
            painter3 = QPainter(pixmap)
            painter3.drawPolygon(self.new_polygon)
        elif self.mode == 'zoom in':
            pixmap = self.base_pixmap.scaled(100,100)
        #self.setPixmap(pixmap)
        painter.drawPixmap(0, 0, pixmap)
"""

class view_project_control(QGroupBox):
    def __init__(self, link=None, parent=None, signal=None):
        super().__init__()
        self.signal = signal
        self.init_ui()
        self.connect_ui()

    def init_ui(self):
        self.btn_previous = QPushButton("0")
        self.btn_next = QPushButton("1")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_previous)
        self.layout.addWidget(self.btn_next)

        self.setLayout(self.layout)

    def connect_ui(self):
        self.btn_previous.clicked.connect(self.on_0)
        self.btn_next.clicked.connect(self.on_1)
    
    def on_0(self):
        self.signal.emit(0)

    def on_1(self):
        self.signal.emit(1)



class view_project(QGraphicsView):
    def __init__(self, parent, file_link=None, signal=None):
        super().__init__(parent = parent)
        self.signal = signal
        self.hdf_file = file_link

        image_as_pixmap = utils.pixmap_at_index(self.hdf_file, 0)
        self.setGeometry(QtCore.QRect(10, 40, 601, 411))
        self.scene = QGraphicsScene()
        self.background = self.scene.addPixmap(image_as_pixmap)
        self.setScene(self.scene)
        self.signal.connect(self.pixmap_change)


    def mousePressEvent(self, event):
        print(event.pos())
        print(self.mapToScene(event.pos()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.scale(1.3, 1.3)
    
    @pyqtSlot(int)
    def pixmap_change(self, index):
        self.scene.removeItem(self.background)
        image_as_pixmap = utils.pixmap_at_index(self.hdf_file, index)
        self.background = self.scene.addPixmap(image_as_pixmap)
        


"""
class canvas_and_features(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.init_canvas()
        self.init_features()
        self.place_canvas_and_features()

    def init_canvas(self):
        self.canvas = QLabel()

        self.pixmap_base = QPixmap()
        self.pixmap_mask = QPixmap()
        self.pixmap_polygon = QPixmap()

        self.polygon_iterations = QPolygon()
        self.polygon_new = QPolygon()
        self.polygon_new_points = []

        #self.scroll = QScrollArea()
        #self.scroll.setWidget(self.canvas)
        #self.scroll.setWidgetResizable(True)
        self.view = QGraphicsView(self.canvas)

        self.mode = 'display base'

    def init_features(self):
        self.btn_zoom_in = QPushButton("Приблизить")
        self.btn_zoom_out = QPushButton("Отдалить")

        self.btn_zoom_in.clicked.connect(self.zoom_in)
        self.btn_zoom_out.clicked.connect(self.zoom_out)

    def place_canvas_and_features(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        #self.layout.addWidget(self.scroll, 0, 0)
        self.layout.addWidget(self.view, 0, 0)
        self.layout.addWidget(self.btn_zoom_in, 0, 1)
        self.layout.addWidget(self.btn_zoom_out, 0, 2)

    def zoom_in(self):
        bar = self.scroll.horizontalScrollBar()
        bar.setValue(10)

    def zoom_out(self):
        x = self.pixmap_base.width()
        y = self.pixmap_base.height()
        size = self.pixmap_base.size()
        size.scale(x * 0.5, y * 0.5, Qt.KeepAspectRatio)
        self.pixmap_base = self.pixmap_base.scaled(size, aspectRatioMode=Qt.KeepAspectRatio)

    def update_base(self, pixmap):
        self.pixmap_base = pixmap.copy()
        self.pixmap_mask = pixmap.copy()
        self.pixmap_polygon = pixmap.copy()

    def paintEvent(self, event):
        #painter = QPainter(self.canvas)
        #painter.setPen(QPen(1))
        pixmap = QPixmap()
        if self.mode == 'display base':
            pixmap = self.pixmap_base
        self.canvas.setPixmap(pixmap)
        #painter.drawPixmap(0, 0, pixmap)

    def mousePressEvent(self, event):
        print(event.pos())
        #print(event.globalPos())
        print(event.screenPos())
        print(event.windowPos())
        #print(event.x())
        #print(event.y())






class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.imgLabel = QLabel(self)
        pixmap = QPixmap("image.jpg")
        self.imgLabel.setPixmap(pixmap)
        self.imgLabel.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.imgLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.imgLabel)
        self.scroll.setWidgetResizable(True)
        #scroll.setFrameShape(QFrame.NoFrame)

        self.zoomInButton = QPushButton('Zoom In', self)
        self.zoomInButton.clicked.connect(self.onZoomIn)

        self.zoomOutButton = QPushButton('Zoom Out', self)
        self.zoomOutButton.clicked.connect(self.onZoomOut)

        self.buttonGroup = QGroupBox()
        vboxButtons = QVBoxLayout()
        vboxButtons.addWidget(self.zoomInButton)
        vboxButtons.addWidget(self.zoomOutButton)
        vboxButtons.addStretch()
        self.buttonGroup.setLayout(vboxButtons)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.scroll)
        self.hbox.addWidget(self.buttonGroup)
        self.setLayout(self.hbox)
        self.init()
        #self.show()

    def init(self):

        self.scaleFactor = 1.0

    def onZoomIn(self):
        self.scaleImage(1.25)

    def onZoomOut(self):
        self.scaleImage(0.8)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        pm = self.imgLabel.pixmap()
        x = pm.width() * self.scaleFactor
        y = pm.width() * self.scaleFactor
        if x > 0 and y > 0:
            pm = pm.scaled(x, y, Qt.KeepAspectRatio)

            self.imgLabel.setPixmap(pm)
"""