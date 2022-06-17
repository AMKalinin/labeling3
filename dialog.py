from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

import classifier
import project
import os
import utils
import cv2
import h5py

class classesTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.chosen = []
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            data = QMimeData()
            drag.setMimeData(data)
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        tree = event.source() 
        if tree == self:
            return
        try:
            widget = tree.currentItem()
            base_index = tree.indexOfTopLevelItem(widget)
            class_index = tree.indexOfTopLevelItem(widget.parent())

            if base_index == -1:
                base = widget.parent()
                base.removeChild(widget)
                tree.chosen.remove(widget.text(1))
                if base.childCount() == 0:
                    base_index = tree.indexOfTopLevelItem(base)
                    tree.takeTopLevelItem(base_index)

            elif class_index == -1:
                base = widget
                base_index = tree.indexOfTopLevelItem(base)
                for index in range(base.childCount()):
                    tree.chosen.remove(base.child(index).text(1))
                tree.takeTopLevelItem(base_index)
        except:
            pass


class selectedClassesTree(classesTree):
    def __init__(self):
        super().__init__()

    def dropEvent(self, event):
        base_in_tree = None
        tree = event.source()
        if tree == self:
            return
        try:
            widget = tree.currentItem()
            base_index = tree.indexOfTopLevelItem(widget)
            class_index = tree.indexOfTopLevelItem(widget.parent())

            if base_index == -1:
                base = widget.parent()
                if widget.text(1) not in self.chosen:
                    self.chosen.append(widget.text(1))
                    base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
                    if not base_in_tree:
                        self.addTopLevelItem(QTreeWidgetItem([base.text(0)]))
                    base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
                    base_in_tree[0].addChild(QTreeWidgetItem([widget.text(0), widget.text(1)]))

            elif class_index == -1:
                base = widget
                base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
                if not base_in_tree:
                    self.addTopLevelItem(QTreeWidgetItem([base.text(0)]))
                    base_in_tree = self.findItems(base.text(0), Qt.MatchExactly)
                    for index in range(base.childCount()):
                        base_in_tree[0].addChild(QTreeWidgetItem([base.child(index).text(0), base.child(index).text(1)]))
                        self.chosen.append(base.child(index).text(1))
                else:
                    for index in range(base.childCount()):
                        if base.child(index).text(1) not in self.chosen:
                            self.chosen.append(base.child(index).text(1))
                            base_in_tree[0].addChild(QTreeWidgetItem([base.child(index).text(0), base.child(index).text(1)]))
            if base_in_tree:
                base_in_tree[0].sortChildren(1, Qt.AscendingOrder)
        except:
            pass

class selectedImagesButton(QPushButton):
    def __init__(self,text, lbl):
        super().__init__(text)
        self.images = lbl
        self.setAcceptDrops(True)
        self.setObjectName("images")
        self.images_list = []

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        img = event.mimeData().text()
        files = img.split('\n')
        if len(files)>1:
            files.pop(-1)
        for i in range(len(files)):
            files[i] = files[i][8:]
        for file in files:
            if (file not in self.images_list) and (file[-5]):
                self.images_list.append(file)
        if len(self.images_list)<5:
            images ="\n".join( [x.split('/')[-1] for x in self.images_list ] )
        else:
            images = f"Выбрано {len(self.images_list)} файлов"
        self.images.setText(images)

class newProject(QDialog):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setWindowTitle("Создание нового проекта")
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
        self.classestree = classesTree()
        self.classestree.setColumnCount(2)
        self.classestree.setHeaderLabels(['Name', 'Code'])
        utils.fill_tree(self.classestree)

        self.selectedclassestree = selectedClassesTree()
        self.selectedclassestree.setColumnCount(2)
        self.selectedclassestree.setHeaderLabels(['Name', 'Code'])

    def init_choose_images(self):
        self.images = QLabel("Выбранные изображения: ")
        self.add = selectedImagesButton("Выберите или перетащите изображения", self.images)

    def on_add(self):
        file_dialog_response = QFileDialog.getOpenFileNames()[0]
        for file in file_dialog_response:
            if file not in self.add.images_list:
                self.add.images_list.append(file)
        if len(self.add.images_list)<5:
            images ="\n".join( [x.split('/')[-1] for x in self.add.images_list ] )
        else:
            images = f"Выбрано файлов: {len(self.add.images_list)}"
        self.images.setText(images)

    def connect_ui(self):
        self.cancel.clicked.connect(self.on_cancel)
        self.ok.clicked.connect(self.on_ok)
        self.add.clicked.connect(self.on_add)

    def set_layouts(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.label_name, 0, 0)
        self.layout.addWidget(self.input_name, 0, 1)
        self.layout.addWidget(self.label_description, 1, 0)
        self.layout.addWidget(self.input_description, 1, 1)
        self.layout.addWidget(self.classestree, 2, 0)
        self.layout.addWidget(self.selectedclassestree, 2, 1)
        self.layout.addWidget(self.add, 3, 0, 1, 2)
        self.layout.addWidget(self.images, 4, 0)
        self.layout.addWidget(self.cancel, 5, 0)
        self.layout.addWidget(self.ok, 5, 1)

    def on_cancel(self):
        self.deleteLater()

    def on_ok(self):
        project = classifier.items.PROJECTS.value + self.input_name.text() + classifier.hdfs.POSTFIX.value
        try:
            with h5py.File(project, 'w-') as hdf:
                hdf.attrs[classifier.hdfs.NAME.value] = self.input_name.text()
                hdf.attrs[classifier.hdfs.DESCRIPTION.value] = self.input_description.text()
                hdf.attrs[classifier.hdfs.CLASSES.value] = self.selectedclassestree.chosen
                hdf.attrs[classifier.hdfs.TASK_COUNT.value] = len(self.add.images_list)
                for image in self.add.images_list:
                    task = hdf.create_dataset(str(self.add.images_list.index(image)), data=cv2.imread(image))
                    task.attrs[classifier.tasks.COUNT.value] = 0
                    task.attrs[classifier.tasks.STATUS.value] = classifier.tasks.TO_DO.value
                    task.attrs[classifier.aerial.SOURCE.value] = 'не задано'
                    task.attrs[classifier.aerial.ALTITUDE.value] = 'не задано'
                    task.attrs[classifier.aerial.LATITUDE.value] = 'не задано'
                    task.attrs[classifier.aerial.LONGITUDE.value] = 'не задано'
                    task.attrs[classifier.aerial.SUN.value] = 'не задано'
                    task.attrs[classifier.aerial.SPATIAL.value] = 'не задано'
                    task.attrs[classifier.aerial.SIZE.value] = 'не задано'
                    task.attrs[classifier.aerial.DATE.value] = 'не задано'
                    task.attrs[classifier.aerial.TIME.value] = 'не задано'
        except FileExistsError:
            message = QMessageBox.about(self, "Ошибка:", "Файл с таким именем уже существует!")
        self.main._parse_projects.emit()
        self.deleteLater()

class basedProject(newProject):
    def __init__(self, main, old_hdf):
        super().__init__(main)
        self.base = old_hdf
        self.read_base()

    def read_base(self):
        with h5py.File(self.base, 'r') as hdf:
            self.selectedclassestree.chosen = [x for x in hdf.attrs[classifier.hdfs.CLASSES.value]]
            utils.fill_tree_with_select_classes(self.selectedclassestree, hdf.attrs[classifier.hdfs.CLASSES.value])
            self.input_name.setText(hdf.attrs[classifier.hdfs.NAME.value]+'(копия)')
            self.input_description.setText('Основан на: '+hdf.attrs[classifier.hdfs.NAME.value])


    def on_ok(self):
        project = classifier.items.PROJECTS.value + self.input_name.text() + classifier.hdfs.POSTFIX.value
        try:
            with h5py.File(project, 'w-') as hdf:
                hdf.attrs[classifier.hdfs.NAME.value] = self.input_name.text()
                hdf.attrs[classifier.hdfs.DESCRIPTION.value] = self.input_description.text()
                hdf.attrs[classifier.hdfs.CLASSES.value] = self.selectedclassestree.chosen
                with h5py.File(self.base, 'r') as hdf_o:
                    count = hdf_o.attrs[classifier.hdfs.TASK_COUNT.value]
                    hdf.attrs[classifier.hdfs.TASK_COUNT.value] = len(self.add.images_list) + count
                    for id in range(count):
                        task = hdf.create_dataset(str(id), data=hdf_o[str(id)])
                        task.attrs[classifier.tasks.COUNT.value] = hdf_o[str(id)].attrs[classifier.tasks.COUNT.value]
                        task.attrs[classifier.tasks.STATUS.value] = hdf_o[str(id)].attrs[classifier.tasks.STATUS.value]
                        count_m = hdf_o[str(id)].attrs[classifier.tasks.COUNT.value]
                        i = 0
                        for id_polygon in range(count_m):
                            cclas = utils.attrs_get_class(hdf_o[str(id)].attrs[str(id_polygon)])
                            if cclas in self.selectedclassestree.chosen:
                                task.attrs[str(id_polygon-i)] = hdf_o[str(id)].attrs[str(id_polygon)]
                            else:
                                i += 1
                for image in self.add.images_list:
                    task = hdf.create_dataset(str(self.add.images_list.index(image)+count), data=cv2.imread(image))
                    task.attrs[classifier.tasks.COUNT.value] = 0
                    task.attrs[classifier.tasks.STATUS.value] = classifier.tasks.TO_DO.value
        except FileExistsError:
            message = QMessageBox.about(self, "Ошибка:", "Файл с таким именем уже существует!")
        self.main._parse_projects.emit()
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
        dialog = segflex_classes_choose.classes_choose(signal=self._project_created_new, project_name=self.name, project_description=self.project_description)
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
