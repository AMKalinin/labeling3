from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import segflex_seg_window as seg_window
import re
import h5py
import segflex_classifier as classifier
import cv2



class project_as_widget(QGroupBox):
    Signal_OneParameter = pyqtSignal(str)
    signal_parse_tasks = pyqtSignal(str)

    def __init__(self,
    name,
    classes,
    path,
    signal,
    signal_open,
    parent=None,
    ide=0):
        #QGroupBox.__init__(self, name, classes, parent, ide)
        super().__init__()
        print("name = " , name, "path = ", path)
        self.path = path
        self.id = ide
        self.signal = signal
        self.signal_op = signal_open

        layout = QHBoxLayout()
        layout_preview = QVBoxLayout()
        layout_info = QVBoxLayout()
        #layout_status = QVBoxLayout()
        #layout_jobs = QVBoxLayout()
        #layout_actions =QVBoxLayout()
        layout_push = QHBoxLayout()

        layout.addLayout(layout_preview)
        layout.addLayout(layout_info)
        #layout.addLayout(layout_status)
        #layout.addLayout(layout_jobs)
        #layout.addLayout(layout_actions)
        layout.addLayout(layout_push)


        image = QLabel(self)
        pixmap = QtGui.QPixmap("img0.jpg")
        image.setPixmap(pixmap)
        image.setFixedSize(100, 100)

        info_block = QLabel()
        info_block.setTextFormat(Qt.RichText)
        info_block.setText('<p>' +
                                '<font size=7>' + 
                                    '<u>' +
                                        name +
                                    '</u>' +
                                '</font>' + 
                                '<br>' + 
                            '</p>' +
                            #'<center>' +
                             #   '__________'
                            #'</center>' +
                            '<br>' + 
                            'second_str' 
                            )

        info_created_by = QLabel("Created by Hashly on November 1st 2021")
        info_last_update = QLabel("Last updated 15 days ago")

        status = QLabel(" ".join(str(classes)))

        jobs = QLabel("0 of 1 jobs")

        self.btn_open = QPushButton("Список задач")
        self.btn_open.clicked.connect(self.on_open)
        self.btn_add = QPushButton("Добавить задачи")
        self.btn_add.clicked.connect(self.on_add)
        self.btn_view = QPushButton("Режим просмотра")
        #self.btn_delete = QPushButton("Delete")
        #self.btn_delete.clicked.connect(self.emit_delete_signal)
        #self.btn_edit = QPushButton("Edit")
        #self.btn_edit.clicked.connect(self.on_edit)
        #actions_bar = QComboBox()
        #actions_bar.addItems(["do smth1", "do smth2"])

        btn_id_in_layout = QPushButton("print id")
        #btn_id_in_layout.clicked.connect()


        layout_preview.addWidget(image)
        layout_info.addWidget(info_block)
        #layout_info.addWidget(info_created_by)
        #layout_info.addWidget(info_last_update)
        #layout_status.addWidget(status)
        #layout_jobs.addWidget(jobs)
        #layout_actions.addWidget(self.btn_open)
        #layout_push.addWidget(self.btn_add)
        layout_push.addWidget(self.btn_open)
        layout_push.addWidget(self.btn_view)

        #layout_actions.addWidget(self.btn_delete)
        #layout_actions.addWidget(self.btn_edit)

        #layout_actions.addWidget(actions_bar)


        self.setMaximumHeight(120)
        self.setLayout(layout)

    def on_add(self):
        task_to_add = QFileDialog.getOpenFileName()[0]
        #match = re.search('[а-яА-Я]', task_to_add)
        #assert match == None, 'cv2.imread need english file name'
        if task_to_add:
            with h5py.File(self.path, 'r+') as hdf:
                group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
                task_count = hdf.attrs[classifier.HDF_FILE_TASK_COUNT]
                task_as_numpy = cv2.imread(task_to_add)
                group_srcs.create_dataset(str(task_count), data=task_as_numpy)
                group_srcs[str(task_count)].attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_0
                group_srcs[str(task_count)].attrs[classifier.HDF_TASK_POLYGON_COUNT] = 0
                hdf.attrs[classifier.HDF_FILE_TASK_COUNT] += 1
            #self.signal_parse_tasks.emit(self.path)
            self.signal.emit(self.path)


    def add_images(self):
        file_dialog_response = QFileDialog.getOpenFileName()[0]
        #match = re.search(r'\p{IsCyrillic}', file_dialog_response) 
        #assert match == None, 'cv2.imread need english file name'
        if file_dialog_response not in self.selected_images_list:
            self.selected_images_list.append(file_dialog_response)
        images = " ".join(self.selected_images_list)
        self.selected_images.setText("Выбранные изображения: " + images)
        #print(self.selected_images_list)

    def create_new_project_file(self): 
        projects_dir = classifier.PROJECTS_FOLDER_FULL_NAME
        project_name = projects_dir + '/' + classifier.current_project.name + classifier.HDF_POSTFIX  #classifier.current_project.name
        with h5py.File(project_name, 'w-') as hdf:
            hdf.attrs[classifier.HDF_FILE_NAME] = classifier.current_project.name
            hdf.attrs[classifier.HDF_FILE_TIME_C] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_TIME_U] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_DESCRIPTION] = classifier.current_project.description
            hdf.attrs[classifier.HDF_FILE_CLASSES] = classifier.current_project.classes
            hdf.attrs[classifier.HDF_FILE_TASK_COUNT] = 0
            hdf.create_group(classifier.HDF_GROUP_SRCS_NAME)
            hdf.create_group(classifier.HDF_GROUP_FEATURES_NAME)
            image_group = hdf.require_group(classifier.HDF_GROUP_SRCS_NAME)
            identifier = 0
            for image_path in self.selected_images_list:
                print(image_path)
                image_as_numpy = cv2.imread(image_path) # neef check for supporting formats
                print(image_as_numpy.shape)
                image_group.create_dataset(str(identifier), data=image_as_numpy)
                #dataset = image_group.require_dataset(str(identifier)) добавление атрибутов в датасет???
                identifier += 1

    def on_open(self):
        #self.signal.emit(self.path)
        self.signal_op.emit(self.path)
        #self.signal_parse_tasks.emit(self.path)
        #pass

    def emit_delete_signal(self):
        #self.Signal_OneParameter.emit("date_str")
        self.deleteLater()

    def on_edit(self):
        self.seg_window = seg_window.seg_window(self, self.path)
        self.seg_window.exec_()
