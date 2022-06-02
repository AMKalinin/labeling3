from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import classifier
import h5py
import utils

class taskWidget(QGroupBox):
    def __init__(self, parent, main, identifier, mode):
        super().__init__(parent = parent)
        self.main = main
        self.identifier = identifier
        self.mode = mode
        self.init_ui()

    def init_ui(self):
        self.check_status()
        self.status = self.main.file[str(self.identifier)].attrs[classifier.tasks.STATUS.value]
        self.adjust_window()
        self.create_layouts()
        self.order_layouts()
        self.init_widgets()
        self.place_widgets()
        #self.fill_layouts()
        #self.place_layouts()
        self.connect_ui()

    def adjust_window(self):
        self.layout = QHBoxLayout()
        self.setMouseTracking(True)
        self.setMaximumHeight(120)
        self.setLayout(self.layout)

    def create_layouts(self):
        self.layout_preview = QVBoxLayout()
        self.layout_actions = QVBoxLayout()
        self.layout_backward = QVBoxLayout()
        self.layout_forward = QVBoxLayout()
        #self.layout_controls = QVBoxLayout()
        self.layout_status = QVBoxLayout()

    def order_layouts(self):
        self.layout.addLayout(self.layout_backward)
        self.layout.addLayout(self.layout_preview)
        self.layout.addLayout(self.layout_status)
        self.layout.addLayout(self.layout_actions)
        self.layout.addLayout(self.layout_forward)

    """
    def fill_layouts(self):
        self.fill_preview()
        self.fill_actions()
        #self.fill_forward()
        #self.fill_backward()
        #self.fill_controls()
    """

    def init_widgets(self):
        self.init_preview()
        self.init_actions()

    def init_preview(self):
        self.preview = QLabel(self)
        pixmap = utils.create_preview(hdf=self.main.file, identifier = self.identifier)
        self.preview.setPixmap(pixmap)

    def init_actions(self):
        tocheck = QIcon(QPixmap(classifier.items.tocheck.value))
        redo = QIcon(QPixmap(classifier.items.redo.value))
        checked = QIcon(QPixmap(classifier.items.checked.value))

        todo = QPixmap(classifier.items.status_todo.value)
        inpr = QPixmap(classifier.items.status_inpr.value)
        toch = QPixmap(classifier.items.status_toch.value)

        self.tocheck = QToolButton()
        self.redo = QToolButton()
        self.checked = QToolButton()

        self.todo = QLabel()
        self.inpr = QLabel()
        self.toch = QLabel()

        self.tocheck.setIcon(tocheck)        
        self.redo.setIcon(redo)        
        self.checked.setIcon(checked)

        self.todo.setPixmap(todo)
        self.inpr.setPixmap(inpr)
        self.toch.setPixmap(toch)

        self.attrs = QPushButton("Редактировать параметры снимка")
        self.edit = QPushButton("Открыть окно сегментации")

    def place_widgets(self):
        self.layout_preview.addWidget(self.preview)
        self.layout_actions.addWidget(self.attrs)
        self.layout_actions.addWidget(self.edit)

        if self.mode == classifier.tasks.LEFT.value:
            self.layout_forward.addWidget(self.tocheck)
            if self.status == classifier.tasks.TO_DO.value:
                self.layout_status.addWidget(self.todo)
            elif self.status == classifier.tasks.IN_PROGRESS.value:
                self.layout_status.addWidget(self.inpr)
        elif self.mode == classifier.tasks.RIGHT.value:
            self.layout_forward.addWidget(self.checked)
            self.layout_backward.addWidget(self.redo)
            self.layout_status.addWidget(self.toch)

    def connect_ui(self):
        self.attrs.clicked.connect(self.on_attrs)
        self.edit.clicked.connect(self.on_edit)
        self.tocheck.clicked.connect(self.on_tocheck)
        self.redo.clicked.connect(self.on_redo)
        self.checked.clicked.connect(self.on_checked)

    def check_status(self):
        count = utils.get_task_polygons(self.main.file, self.identifier)
        if (count != 0 and
            self.main.file[str(self.identifier)].attrs[classifier.tasks.STATUS.value] != classifier.tasks.TO_CHECK.value and
            self.main.file[str(self.identifier)].attrs[classifier.tasks.STATUS.value] != classifier.tasks.DONE.value):
            self.main.file[str(self.identifier)].attrs[classifier.tasks.STATUS.value] = classifier.tasks.IN_PROGRESS.value


    def on_attrs(self):
        pass

    def on_edit(self):
        self.main._edit_task.emit(self.identifier)
        self.main.tab.parse_tasks()

    def on_tocheck(self):
        self.main.file[str(self.identifier)].attrs[classifier.tasks.STATUS.value] = classifier.tasks.TO_CHECK.value
        self.main.tab.parse_tasks()

    def on_redo(self):
        self.main.file[str(self.identifier)].attrs[classifier.tasks.STATUS.value] = classifier.tasks.IN_PROGRESS.value
        self.main.tab.parse_tasks()

    def on_checked(self):
        self.main.file[str(self.identifier)].attrs[classifier.tasks.STATUS.value] = classifier.tasks.DONE.value
        self.main.tab.parse_tasks()
        self.main.tab.parse_projects()




    """
    def place_layouts(self):
        #self.layout.addLayout(self.layout_backward)
        self.layout.addLayout(self.layout_preview)
        #self.layout.addLayout(self.layout_controls)
        #self.layout.addLayout(self.layout_info)
        self.layout.addLayout(self.layout_actions)
        self.layout.addLayout(self.layout_forward)
        self.layout.addLayout(self.layout_backward)
        self.layout.addLayout(self.layout_status)
        self.layout_preview.addWidget(self.preview)
        #self.layout_info.addWidget(self.info_number)
        #self.layout_info.addWidget(self.info_created_by)
        #self.layout_info.addWidget(self.info_last_update)
        #self.layout_forward.addWidget(self.forward_btn)
        #self.layout_backward.addWidget(self.backward_btn)
        #self.layout_controls.addWidget(self.conttrol_1_btn)
        #self.layout_controls.addWidget(self.conttrol_2_btn)
        #if self.mode == classifier.TASK_WIDGET_MODE_0:
            #self.layout_backward.addWidget(self.delete_btn)
            #self.layout_actions.addWidget(self.btn_edit)
            #self.layout_actions.addWidget(self.btn_tocheck)
        #if self.mode == classifier.TASK_WIDGET_MODE_1:
            #self.layout_actions.addWidget(self.btn_redo)
            #self.layout_actions.addWidget(self.btn_done)
        if self.mode == classifier.tasks.LEFT.value:
            self.layout_forward.addWidget(self.tocheck)
            if self.status == classifier.tasks.TO_DO.value:
                self.layout_status.addWidget(self.todo)
            elif self.status == classifier.tasks.IN_PROGRESS.value:
                self.layout_status.addWidget(self.inpr)
        elif self.mode == classifier.tasks.RIGHT.value:
            self.layout_forward.addWidget(self.checked)
            self.layout_backward.addWidget(self.redo)
            self.layout_status.addWidget(self.toch)
        """






    def enterEvent(self, event):
        print("enterEvent")
    
    def leaveEvent(self, event):
        print("leaveEvent")

"""
#LEGACY CODE BELOW THIS LINE 
class task_widget(QGroupBox):
    def __init__(self, path, identifier, mode, signal):
        super().__init__()
        self.project_path = path
        self.identifier = identifier
        self.mode = mode
        self.signal = signal
        self.unit_ui()

    def unit_ui(self):
        self.create_layouts()
        self.fill_layouts()
        self.place_layouts()
        self.connect_ui()
        self.adjust_window()
    
    def connect_ui(self):
        self.conttrol_2_btn.clicked.connect(self.on_edit)
        if self.mode == classifier.TASK_WIDGET_MODE_0:
            self.backward_btn.clicked.connect(self.on_delete_task)
            self.forward_btn.clicked.connect(self.on_tocheck)
        if self.mode == classifier.TASK_WIDGET_MODE_1:
            self.backward_btn.clicked.connect(self.on_redo)


    def create_layouts(self):
        self.layout = QHBoxLayout()
        self.layout_preview = QVBoxLayout()
        #self.layout_info = QVBoxLayout()
        self.layout_actions = QVBoxLayout()
        self.layout_backward = QVBoxLayout()
        self.layout_forward = QVBoxLayout()
        self.layout_controls = QVBoxLayout()

    def fill_layouts(self):
        self.fill_preview()
        #self.fill_info()
        self.fill_actions()
        #self.fill_delete()
        self.fill_forward()
        self.fill_backward()
        self.fill_controls()

    def place_layouts(self):
        self.layout.addLayout(self.layout_backward)
        self.layout.addLayout(self.layout_preview)
        self.layout.addLayout(self.layout_controls)
        #self.layout.addLayout(self.layout_info)
        self.layout.addLayout(self.layout_actions)
        self.layout.addLayout(self.layout_forward)
        self.layout_preview.addWidget(self.preview)
        #self.layout_info.addWidget(self.info_number)
        #self.layout_info.addWidget(self.info_created_by)
        #self.layout_info.addWidget(self.info_last_update)
        self.layout_forward.addWidget(self.forward_btn)
        self.layout_backward.addWidget(self.backward_btn)
        self.layout_controls.addWidget(self.conttrol_1_btn)
        self.layout_controls.addWidget(self.conttrol_2_btn)
        #if self.mode == classifier.TASK_WIDGET_MODE_0:
            #self.layout_backward.addWidget(self.delete_btn)
            #self.layout_actions.addWidget(self.btn_edit)
            #self.layout_actions.addWidget(self.btn_tocheck)
        #if self.mode == classifier.TASK_WIDGET_MODE_1:
            #self.layout_actions.addWidget(self.btn_redo)
            #self.layout_actions.addWidget(self.btn_done)


    def adjust_window(self):
        self.setMouseTracking(True)
        self.setMaximumHeight(120)
        self.setLayout(self.layout)
    
    def fill_preview(self):
        self.preview = QLabel(self)
        pixmap = self.create_previw()
        self.preview.setPixmap(pixmap)

    def fill_info(self):
        self.info_number = QLabel("#" )#+ name)
        self.info_created_by = QLabel("Created by Hashly on November 1st 2021")
        self.info_last_update = QLabel("Last updated 15 days ago")
    
    def fill_delete(self):
        self.delete_btn = QToolButton()
        self.delete_btn.setFixedSize(100,100)
        delete_icon = QIcon()
        #delete_pixmap = QPixmap(100,100)
        #delete_pixmap.load(classifier.ICON_DELETE_TASK_FULL)
        #delete_icon.addPixmap(delete_pixmap)
        delete_icon.addPixmap(QPixmap(classifier.ICON_DELETE_TASK_FULL))
        self.delete_btn.setIcon(delete_icon)
    
    def fill_backward(self):
        self.backward_btn = QToolButton()
        backward_icon = QIcon()
        if self.mode == classifier.TASK_WIDGET_MODE_0:
            backward_icon.addPixmap(QPixmap(classifier.ICON_BACKWARD_DELETE_TASK_FULL))
        if self.mode == classifier.TASK_WIDGET_MODE_1:
            backward_icon.addPixmap(QPixmap(classifier.ICON_BACKWARD_PASS_TASK_FULL))
        self.backward_btn.setIcon(backward_icon)


    def fill_forward(self):
        self.forward_btn = QToolButton()
        forward_icon = QIcon()
        if self.mode == classifier.TASK_WIDGET_MODE_0:
            forward_icon.addPixmap(QPixmap(classifier.ICON_FORWARD_PASS_TASK_FULL))
        if self.mode == classifier.TASK_WIDGET_MODE_1:
            forward_icon.addPixmap(QPixmap(classifier.ICON_FORWARD_CHECK_TASK_FULL))
        self.forward_btn.setIcon(forward_icon)

    def fill_controls(self):
        self.conttrol_1_btn = QPushButton()
        self.conttrol_2_btn = QPushButton()
        if self.mode == classifier.TASK_WIDGET_MODE_0:
            self.conttrol_1_btn.setText("Параметры")
            self.conttrol_2_btn.setText("Разметка")
        if self.mode == classifier.TASK_WIDGET_MODE_1:
            self.conttrol_1_btn.setText("Параметры")
            self.conttrol_2_btn.setText("Разметка")


    def fill_actions(self):
        if self.mode == classifier.TASK_WIDGET_MODE_0:
            self.btn_tocheck = QPushButton("Отправить модератору")
            self.btn_tocheck.clicked.connect(self.on_tocheck)
            self.btn_edit = QPushButton("Разметить")
            self.btn_edit.clicked.connect(self.on_edit)
        if self.mode == classifier.TASK_WIDGET_MODE_1:
            self.btn_redo = QPushButton("Вернуть на доработку")
            self.btn_redo.clicked.connect(self.on_redo)
            self.btn_done = QPushButton("Готово")
            self.btn_done.clicked.connect(self.on_edit)

    def create_previw(self): 
        with h5py.File(self.project_path, 'r') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            dataset = group_srcs[str(self.identifier)]
            image_as_numpy = dataset[()]
            height, width, channel = image_as_numpy.shape
            bytesPerLine = 3 * width
            image_as_qimage = QImage(image_as_numpy, width, height, bytesPerLine, QImage.Format_RGB888)
            image_correct_rgb = image_as_qimage.rgbSwapped()
            image_as_pixmap = QPixmap(image_correct_rgb)
            image_resized = image_as_pixmap.scaled(100, 100)

            return image_resized

    def on_delete_task(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]
            del group[str(self.identifier)]
            for index in range(self.identifier, hdf.attrs[classifier.HDF_FILE_TASK_COUNT] - 1):
                group[str(index)] = group[str(index + 1)]
                del group[str(index + 1)]
            hdf.attrs[classifier.HDF_FILE_TASK_COUNT] -= 1
        self.deleteLater()
        self.signal.emit(self.project_path)

    def on_redo(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_1
        self.signal.emit(self.project_path)

    def on_done(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_3
        self.signal.emit(self.project_path)

    def on_tocheck(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_2
        self.signal.emit(self.project_path)

    def on_edit(self):
        pass
        self.seg_window = seg_window.seg_window(self, self.project_path)
        self.seg_window.exec_()


    def emit_delete_signal(self):
        #self._OneParameter.emit("date_str")
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_2
        self.deleteLater()

"""




