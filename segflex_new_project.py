from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy)

import segflex_classes_choose
from PyQt5.QtCore import pyqtSignal
import segflex_main
import segflex_classifier as classifier
import os


class new_project_dialog_new(QDialog):
    def __init__(self, signal, parent=None):
        super().__init__()
        self.signal_project_created_new = signal
        self.project_name = '_default_name_'
        self.project_description = '_default_description_'
        self.init_ui()

    def init_ui(self):
        self.adjust_window()
        self.init_buttons()
        self.connect_ui()
        self.set_layouts()

    def adjust_window(self):
        self.setWindowTitle("Создание нового проекта")

    def init_buttons(self):
        self.btn_cancel = QPushButton("Отмена")
        self.btn_ok = QPushButton("ОК")

        self.label_name = QLabel("Название проекта:")
        self.label_description = QLabel("Описание проекта:")

        self.text_area_name = QLineEdit()
        self.text_area_description = QLineEdit()

    def connect_ui(self):
        self.text_area_name.editingFinished.connect(self.set_project_name)
        self.text_area_description.editingFinished.connect(self.set_project_description)

        self.btn_cancel.clicked.connect(self.on_btn_cancel)
        self.btn_ok.clicked.connect(self.on_btn_ok)

    def set_layouts(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        layout_buttons = QHBoxLayout()
        layout_name = QHBoxLayout()
        layout_description = QHBoxLayout()

        layout_buttons.addWidget(self.btn_cancel)
        layout_buttons.addWidget(self.btn_ok)

        layout_name.addWidget(self.label_name)
        layout_name.addWidget(self.text_area_name)

        layout_description.addWidget(self.label_description)
        layout_description.addWidget(self.text_area_description)

        self.layout.addLayout(layout_name)
        self.layout.addLayout(layout_description)
        self.layout.addLayout(layout_buttons)

    def on_btn_cancel(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.close()

    def on_btn_ok(self):
        dialog = segflex_classes_choose.classes_choose(signal=self.signal_project_created_new, project_name=self.project_name, project_description=self.project_description)
        dialog.exec_()
        self.deleteLater()
        

    def is_name_unique(self):
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        if self.text_area_name.text() + '.hdf5' in projects_list:
            self.btn_ok.setDisabled(True)
        else:
            self.btn_ok.setEnabled(True)
            
    def set_project_name(self):
        self.is_name_unique()
        self.project_name = self.text_area_name.text()
    
    def set_project_description(self):
        self.project_description = self.text_area_description.text()

    


class new_project_dialog(QDialog): #qformlayout???
    signal1 = pyqtSignal()
    def __init__(self, signal, parent=None):
        QDialog.__init__(self, parent)
        self.signal = signal
        #print(segflex_main.ggg)
        self.adjust_window()
        self.create_place_buttons()

    def create_place_buttons(self):
        btn_cancel = QPushButton("Отмена")
        self.btn_ok = QPushButton("ОК")
        label_name = QLabel("Название проекта:")
        #label_path = QLabel("Путь хранения:")
        label_description = QLabel("Описание проекта:")
        self.text_area_name = QLineEdit()
        self.text_area_description = QLineEdit()
        #text_area_path = QLineEdit()

        self.text_area_name.editingFinished.connect(self.set_project_name)
        self.text_area_description.editingFinished.connect(self.set_project_description)

        btn_cancel.clicked.connect(self.on_cancel)
        self.btn_ok.clicked.connect(self.on_seg_class_choose)

        layout_buttons = QHBoxLayout()
        layout_name = QHBoxLayout()
        layout_path = QHBoxLayout()
        layout_description = QHBoxLayout()

        layout_buttons.addWidget(btn_cancel)
        layout_buttons.addWidget(self.btn_ok)
        layout_name.addWidget(label_name)
        layout_name.addWidget(self.text_area_name)

        layout_description.addWidget(label_description)
        layout_description.addWidget(self.text_area_description)
        
        #layout_path.addWidget(label_path)
        #layout_path.addWidget(text_area_path)

        self.layout.addLayout(layout_name)
        self.layout.addLayout(layout_description)
        #self.layout.addLayout(layout_path)
        self.layout.addLayout(layout_buttons)

    def check_project_name(self):
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        if self.text_area_name.text() + '.hdf5' in projects_list:
            self.btn_ok.setDisabled(True)
        else:
            self.btn_ok.setEnabled(True)
            

    def set_project_name(self):
        self.check_project_name()
        classifier.current_project.name = self.text_area_name.text()
        print(classifier.current_project.name)
    
    def set_project_description(self):
        classifier.current_project.description = self.text_area_description.text()
        print(classifier.current_project.description)


    def adjust_window(self):
        self.setWindowTitle("Создание нового проекта")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def on_seg_class_choose(self):
        dialog = segflex_classes_choose.classes_choose(signal=self.signal)
        #dialog.signal.connect(self.gosignal)
        #dialog.signal1.connect(self.gosignal)
        dialog.exec_()
        self.deleteLater()
        
    def gosignal(self):
        self.signal.emit()
        self.deleteLater()

    def on_cancel(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.close()



