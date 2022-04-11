from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint#, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar, QMessageBox)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon

import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier
import segflex_seg_label as seg_label
import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple


class seg_window(QDialog):
    def __init__(self, parent=None, path=None):
        QDialog.__init__(self, parent)
        self.project_path = path
        self.identifier = 0
        self.current_image_position = 1
        self.images_dir = classifier.IMAGES_FOLDER_NAME_FULL
        self.instrument_name = "<QPolygon>"
        self.object_class = "__" + classifier.code_100[0] + "__"
       
        self.adjust_window()
        self.open_image(self.identifier)

        self.CNB_create_navigation_bar()
        self.CDIB_create_drawing_instrument_bar()
        self.CCB_create_control_btns()

    def CCB_create_control_btns(self):
        edit_btn = QPushButton("Сегментировать")
        edit_btn.clicked.connect(self.on_edit)

        self.show_existing_mask_button = QPushButton("Показать маску")
        self.show_existing_mask_button.setCheckable(True)
        self.show_existing_mask_button.setChecked(False)
        self.show_existing_mask_button.toggled["bool"].connect(self.CCB_on_show_existing_mask_button)

        self.layout.addWidget(edit_btn, 1, 2)
        self.layout.addWidget(self.show_existing_mask_button, 2, 2)
    
    def CCB_on_show_existing_mask_button(self, status):
        if status == True:
            self.show_existing_mask_button.setChecked(True)
            self.CCB_overlay_existing_mask()
        else:
            self.show_existing_mask_button.setChecked(False)
            self.CCB_hide_existing_mask()

    def CCB_overlay_existing_mask(self):
        self.CCB_parse_current_image_attrs()
        print("objects parsed")

    def CCB_hide_existing_mask(self):
        self.display.restore_srcs()
        print("maska skrita")

    def CCB_parse_current_image_attrs(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            image_srcs = group_srcs[str(self.identifier)]
            current_object_index = int(image_srcs.attrs[classifier.HDF_TASK_POLYGON_COUNT])

            for index in range(1, current_object_index + 1):
                    polygon = QPolygon()
                    tmp_str1 = image_srcs.attrs[str(index)]
                    tmp_str2 = re.sub(r' ', '', tmp_str1)
                    tmp_list = re.findall(r'\([0-9]+,[0-9]+\)', tmp_str2)
                    tuple_list = []
                    for pair in tmp_list:
                        tuple_list.append(make_tuple(pair))
                    for int_pair in tuple_list:
                        polygon.append(QPoint(int_pair[0], int_pair[1]))

                    self.display.overlay_mask(polygon)
                    print("index = ", index, "curoi = ", current_object_index)

    



    def on_edit(self):
        self.drawing_dialog = draw.drawing_dialog(  canvas_pixmap=self.display.base_pixmap,
                                                    canvas_geometry = self.display.geometry(),
                                                    window_geometry=self.geometry(),
                                                    project_path = self.project_path,
                                                    identifier = self.identifier
                                                    )
        self.drawing_dialog.exec_()


    def CDIB_create_drawing_instrument_bar(self):
        drawing_instrument_bar = QToolBar()

        self.pencil_btn = QToolButton()
        self.pencil_btn.setCheckable(True)
        self.pencil_btn.setChecked(False)
        pencil_icon = QIcon()
        pencil_icon.addPixmap(QPixmap(classifier.ICON_PENCIL_TBTN_DRAW_INSTRUMENT_FULL))
        self.pencil_btn.setIcon(pencil_icon)

        self.polygon_btn = QToolButton()
        self.polygon_btn.setCheckable(True)
        self.polygon_btn.setChecked(False)
        polygon_icon = QIcon()
        polygon_icon.addPixmap(QPixmap(classifier.ICON_POLYGON_TBTN_DRAW_INSTRUMENT_FULL))
        self.polygon_btn.setIcon(polygon_icon)

        self.cancel_btn = QToolButton()
        self.cancel_btn.setEnabled(False)
        cancel_icon = QIcon()
        cancel_icon.addPixmap(QPixmap(classifier.ICON_CANCEL_TBTN_DRAW_INSTRUMENT_FULL))
        self.cancel_btn.setIcon(cancel_icon)

        self.save_to_attrs_btn = QToolButton()
        self.save_to_attrs_btn.setEnabled(False)
        save_to_attrs_icon = QIcon()
        save_to_attrs_icon.addPixmap(QPixmap(classifier.ICON_SAVE_TO_ATTRS_TBTN_FULL))
        self.save_to_attrs_btn.setIcon(save_to_attrs_icon)

        drawing_instrument_bar.addWidget(self.pencil_btn)
        drawing_instrument_bar.addWidget(self.polygon_btn)
        drawing_instrument_bar.addWidget(self.cancel_btn)
        drawing_instrument_bar.addWidget(self.save_to_attrs_btn)

        self.pencil_btn.toggled["bool"].connect(self.CDIB_on_pencil_btn)
        self.polygon_btn.toggled["bool"].connect(self.CDIB_on_polygon_btn)
        self.cancel_btn.clicked.connect(self.CDIB_on_cancel_btn)
        self.save_to_attrs_btn.clicked.connect(self.CDIB_on_save_to_attrs_btn)

        self.layout.addWidget(drawing_instrument_bar, 1, 1, 1, 2)

    def CDIB_on_pencil_btn(self, checked):
        if checked:
            self.display.mode = 'pencil_drawing'
            self.save_to_attrs_btn.setEnabled(True)
        if not checked:
            self.CDIB_discard_drawing()
            self.cancel_btn.setCheckable(False)
            self.save_to_attrs_btn.setEnabled(False)

    def CDIB_on_polygon_btn(self, checked):
        if checked:
            self.display.mode = 'draw polygon'
            self.cancel_btn.setEnabled(True)
            self.save_to_attrs_btn.setEnabled(True)
            self.display.repaint()
        if not checked:
            self.CDIB_discard_drawing()
            self.display.update_base(self.display.base_pixmap)
            self.cancel_btn.setEnabled(False)
            self.save_to_attrs_btn.setEnabled(False)

    def CDIB_on_cancel_btn(self, checked):
        if self.display.new_polygon_points:
            self.display.new_polygon_points.pop()
            self.display.update_base(self.display.base_pixmap)
            print("go back")
            self.display.update()

    def CDIB_discard_drawing(self):
        self.display.new_polygon_points.clear()
        self.display.mode = 'display base'
        self.display.repaint()

    def CDIB_on_save_to_attrs_btn(self):
        message = QMessageBox()
        if not self.display.new_polygon_points:
            message.setText("No points in new polygon!")
            message.exec_()
        else:#
            with h5py.File(self.project_path, 'r+') as hdf:
                group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
                image_srcs = group_srcs[str(self.identifier)]
                current_attr_index = int(image_srcs.attrs[classifier.HDF_TASK_POLYGON_COUNT])
                current_attr_index += 1
                image_srcs.attrs[str(current_attr_index)] = (self.object_class + 
                                                            self.instrument_name + 
                                                            self.CDIB_prepare_coords_string_for_saving())
                image_srcs.attrs[classifier.HDF_TASK_POLYGON_COUNT] = str(current_attr_index)
                if image_srcs.attrs[classifier.HDF_TASK_STATUS] == classifier.HDF_TASK_STATUS_0:
                    image_srcs.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_1 #изменение статуса туду - ин ворк
                    print("changed status")
            self.display.new_polygon_points.clear() #
            self.display.mode = 'display mask'
            #self.display.repaint()
            self.CCB_parse_current_image_attrs()
            message.setText("New polygon added to mask")
            message.exec_()

    def CDIB_prepare_coords_string_for_saving(self):
        base = str(self.display.new_polygon_points)
        rtn = re.sub(r'PyQt5.QtCore.QPoint', '', base) 
        #print(rtn)

        return rtn
    """
    def CPB_create_polygon_bar(self):
        polygon_layout = QVBoxLayout()
        with h5py.File(self.project_path, 'r+') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            image_srcs = group_srcs[str(self.identifier)]
            current_object_index = int(image_srcs.attrs[classifier.HDF_TASK_POLYGON_COUNT])

            for index in range(1, current_object_index + 1):
    """


    def CNB_create_navigation_bar(self):
        navigation_bar = QToolBar()

        previous_btn = QToolButton()
        previous_icon = QIcon()
        previous_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_PREVIOUS_FULL))
        previous_btn.setIcon(previous_icon)

        to_first_btn = QToolButton()
        to_first_icon = QIcon()
        to_first_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_TOFIRST_FULL))
        to_first_btn.setIcon(to_first_icon)

        to_last_btn = QToolButton()
        to_last_icon = QIcon()
        to_last_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_TOLAST_FULL))
        to_last_btn.setIcon(to_last_icon)

        next_btn = QToolButton()
        next_icon = QIcon()
        next_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_NEXT_FULL))
        next_btn.setIcon(next_icon)

        self.image_position_postfix = ' / ' + str(self.image_position_max) 
        self.image_position_widget = QLabel(str(self.current_image_position) + self.image_position_postfix) 

        navigation_bar.addWidget(to_first_btn)
        navigation_bar.addWidget(previous_btn)
        navigation_bar.addWidget(next_btn)
        navigation_bar.addWidget(to_last_btn)
        navigation_bar.addWidget(self.image_position_widget)

        to_first_btn.clicked.connect(self.CNB_on_to_first)
        previous_btn.clicked.connect(self.CNB_on_previous)
        next_btn.clicked.connect(self.CNB_on_next)
        to_last_btn.clicked.connect(self.CNB_on_to_last)

        self.layout.addWidget(navigation_bar, 0, 0, 1, 2)#, Qt.AlignTop)# | Qt.AlignHCenter) #области  

        
    def CNB_on_to_first(self):
        if self.identifier != 0:
            self.identifier = 0
            self.current_image_position = 1
            self.open_image(self.identifier)
            self.CNB_update_image_position_widget()

    def CNB_on_to_last(self):
        if self.identifier != self.identifier_max:
            self.identifier = self.identifier_max
            self.current_image_position = self.image_position_max
            self.open_image(self.identifier)
            self.CNB_update_image_position_widget()

    def CNB_on_previous(self):
        if self.identifier > 0:
            self.identifier -= 1
            self.current_image_position -= 1
            self.open_image(self.identifier)
            self.CNB_update_image_position_widget()

    def CNB_on_next(self):
        if self.identifier < self.identifier_max:
            self.identifier += 1
            self.current_image_position += 1
            self.open_image(self.identifier)
            self.CNB_update_image_position_widget()
    
    def CNB_update_image_position_widget(self):
        self.image_position_widget.setText(str(self.current_image_position) + self.image_position_postfix)


    def open_image(self, identifier): 
        self.clear_window_layout(self.image_layout)
        self.display = seg_label.Label()
        self.display.setFixedSize(600,600)
        with h5py.File(self.project_path, 'r') as hdf:
            self.identifier_max = len(list(hdf[classifier.HDF_GROUP_SRCS_NAME].keys())) - 1 #starting with 0
            self.image_position_max = self.identifier_max + 1 #starting with 1
            print(list(hdf[classifier.HDF_GROUP_SRCS_NAME].keys()))
            print(self.identifier_max)
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            dataset = group_srcs[str(identifier)]
            image_as_numpy = dataset[()]
            height, width, channel = image_as_numpy.shape
            bytesPerLine = 3 * width
            image_as_qimage = QImage(image_as_numpy, width, height, bytesPerLine, QImage.Format_RGB888)
            image_correct_rgb = image_as_qimage.rgbSwapped()
            image_as_pixmap = QPixmap(image_correct_rgb)
            self.display.update_base(image_as_pixmap)
            self.image_layout.addWidget(self.display)


    def adjust_window(self):
        self.setWindowTitle("Выбор изображения")
        self.setFixedSize(800,800)
        self.layout = QGridLayout()
        self.image_layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.image_layout, 2, 1) # правильно растянуть область изображения

    def clear_window_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)