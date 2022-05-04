from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal
import classifier
import os
import utils
import select_classes as tree
import cv2
import h5py


class new_project_dialog_new(QDialog):
    def __init__(self, signal):
        super().__init__()
        self.setWindowTitle("Создание нового проекта")
        self.signal = signal
        self.init_ui()

    def init_ui(self):
        self.init_buttons()
        self.init_choose_classes()
        self.init_choose_images()
        self.connect_ui()
        self.set_layouts()

    def init_buttons(self):
        self.cancel = QPushButton("Отмена")
        self.ok = QPushButton("ОК")
        self.label_name = QLabel("Название проекта:")
        self.label_description = QLabel("Описание проекта:")
        self.input_name = QLineEdit()
        self.input_description = QLineEdit()

    def init_choose_classes(self):
        self.all_classes = tree.all_classes()
        self.all_classes.setColumnCount(2)
        self.all_classes.setHeaderLabels(['Name', 'Code'])
        utils.fill_tree(self.all_classes)

        self.classes = tree.selected_classes()
        self.classes.setColumnCount(2)
        self.classes.setHeaderLabels(['Name', 'Code'])

    def init_choose_images(self):
        self.images = QLabel("Выбранные изображения: ")
        self.images_list = []
        self.image_add = QPushButton("Добавить изображение")

    def add_images(self):
        file_dialog_response = QFileDialog.getOpenFileName()[0]
        if file_dialog_response not in self.images_list:
            self.images_list.append(file_dialog_response)
        images = " ".join(self.images_list)
        self.images.setText("Выбранные изображения: " + images)

    def connect_ui(self):
        self.cancel.clicked.connect(self.on_btn_cancel)
        self.ok.clicked.connect(self.on_btn_ok)
        self.image_add.clicked.connect(self.add_images)

    def set_layouts(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.label_name, 0, 0)
        self.layout.addWidget(self.input_name, 0, 1)
        self.layout.addWidget(self.label_description, 1, 0)
        self.layout.addWidget(self.input_description, 1, 1)
        self.layout.addWidget(self.all_classes, 2, 0)
        self.layout.addWidget(self.classes, 2, 1)
        self.layout.addWidget(self.images, 3, 0, 1, 2)
        self.layout.addWidget(self.image_add, 4, 0)
        self.layout.addWidget(self.cancel, 5, 0)
        self.layout.addWidget(self.ok, 5, 1)

    def on_btn_cancel(self):
        self.deleteLater()

    def on_btn_ok(self):
        project = classifier.items.PROJECTS.value + self.input_name.text() + classifier.hdfs.POSTFIX.value
        try:
            with h5py.File(project, 'w-') as hdf:
                hdf.attrs[classifier.hdfs.NAME.value] = self.input_name.text()
                hdf.attrs[classifier.hdfs.DESCRIPTION.value] = self.input_description.text()
                hdf.attrs[classifier.hdfs.CLASSES.value] = self.classes.chosen
                hdf.attrs[classifier.hdfs.TASK_COUNT.value] = len(self.images_list)
                for image in self.images_list:
                    task = hdf.create_dataset(str(self.images_list.index(image)), data=cv2.imread(image))
                    task.attrs[classifier.tasks.COUNT.value] = 0
                    task.attrs[classifier.tasks.STATUS.value] = classifier.tasks.TO_DO.value
        except FileExistsError:
            message = QMessageBox.about(self, "Ошибка:", "Файл с таким именем уже существует!")
        self.signal.emit()
        self.deleteLater()


    """
    def create_new_project_file(self): 
        projects_dir = classifier.PROJECTS_FOLDER_FULL_NAME
        #project_name = projects_dir + '/' + classifier.current_project.name + classifier.HDF_POSTFIX  #classifier.current_project.name
        project_name = projects_dir + '/' + self.name + classifier.HDF_POSTFIX
        with h5py.File(project_name, 'w-') as hdf:
            #hdf.attrs[classifier.HDF_FILE_NAME] = classifier.current_project.name
            hdf.attrs[classifier.HDF_FILE_NAME] = self.name
            hdf.attrs[classifier.HDF_FILE_TIME_C] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_TIME_U] = time.localtime()
            #hdf.attrs[classifier.HDF_FILE_DESCRIPTION] = classifier.current_project.description
            hdf.attrs[classifier.HDF_FILE_DESCRIPTION] = self.description
            hdf.attrs[classifier.HDF_FILE_CLASSES] = classifier.current_project.classes
            hdf.attrs[classifier.HDF_FILE_TASK_COUNT] = 0
            #hdf.create_group(classifier.HDF_GROUP_SRCS_NAME)
            #hdf.create_group(classifier.HDF_GROUP_FEATURES_NAME)
            #image_group = hdf.require_group(classifier.HDF_GROUP_SRCS_NAME)
            identifier = 0
            if self.selected_images_list:
                for image_path in self.selected_images_list:
                    print(image_path)
                    image_as_numpy = cv2.imread(image_path) # neef check for supporting formats
                    print(image_as_numpy.shape)
                    #image_group.create_dataset(str(identifier), data=image_as_numpy)
                    #image_group[str(identifier)].attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_0

                    hdf.create_dataset(str(identifier), data=image_as_numpy)
                    hdf[str(identifier)].attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_0

                    #dataset = image_group.require_dataset(str(identifier)) добавление атрибутов в датасет???
                    identifier += 1
                    hdf.attrs[classifier.HDF_FILE_TASK_COUNT] += 1
    """

    """
        dialog = segflex_classes_choose.classes_choose(signal=self.signal_project_created_new, project_name=self.name, project_description=self.project_description)
        dialog.exec_()
        self.deleteLater()
    """
    """
    def is_name_unique(self):
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        if self.input_name.text() + '.hdf5' in projects_list:
            self.ok.setDisabled(True)
        else:
            self.ok.setEnabled(True)
            
    def set_project_name(self):
        self.is_name_unique()
        self.name = self.input_name.text()
    
    def set_project_description(self):
        self.project_description = self.input_description.text()
    """
