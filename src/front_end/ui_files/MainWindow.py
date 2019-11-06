# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 855)
        self.mode_frame = QtWidgets.QFrame(MainWindow)
        self.mode_frame.setGeometry(QtCore.QRect(50, 20, 411, 111))
        self.mode_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mode_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mode_frame.setObjectName("mode_frame")
        self.label_load_2 = QtWidgets.QLabel(self.mode_frame)
        self.label_load_2.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.label_load_2.setObjectName("label_load_2")
        self.radio_echo = QtWidgets.QRadioButton(self.mode_frame)
        self.radio_echo.setGeometry(QtCore.QRect(10, 30, 161, 20))
        self.radio_echo.setObjectName("radio_echo")
        self.radio_machine_learning = QtWidgets.QRadioButton(self.mode_frame)
        self.radio_machine_learning.setGeometry(QtCore.QRect(10, 60, 191, 20))
        self.radio_machine_learning.setObjectName("radio_machine_learning")
        self.files_frame = QtWidgets.QFrame(MainWindow)
        self.files_frame.setGeometry(QtCore.QRect(50, 150, 411, 501))
        self.files_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.files_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.files_frame.setObjectName("files_frame")
        self.label_load = QtWidgets.QLabel(self.files_frame)
        self.label_load.setGeometry(QtCore.QRect(10, 20, 76, 16))
        self.label_load.setObjectName("label_load")
        self.btn_load_file = QtWidgets.QPushButton(self.files_frame)
        self.btn_load_file.setGeometry(QtCore.QRect(90, 10, 171, 32))
        self.btn_load_file.setObjectName("btn_load_file")
        self.table_widget = QtWidgets.QTableWidget(self.files_frame)
        self.table_widget.setGeometry(QtCore.QRect(0, 80, 401, 421))
        self.table_widget.setMinimumSize(QtCore.QSize(401, 0))
        self.table_widget.setMaximumSize(QtCore.QSize(401, 16777215))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, item)
        self.btn_start_echo = QtWidgets.QPushButton(self.files_frame)
        self.btn_start_echo.setGeometry(QtCore.QRect(90, 40, 171, 32))
        self.btn_start_echo.setObjectName("btn_start_echo")
        self.scrollArea = QtWidgets.QScrollArea(MainWindow)
        self.scrollArea.setGeometry(QtCore.QRect(520, 20, 691, 781))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea_widget = QtWidgets.QWidget()
        self.scrollArea_widget.setGeometry(QtCore.QRect(0, 0, 689, 779))
        self.scrollArea_widget.setObjectName("scrollArea_widget")
        self.scrollArea.setWidget(self.scrollArea_widget)
        self.btn_save_file = QtWidgets.QPushButton(MainWindow)
        self.btn_save_file.setGeometry(QtCore.QRect(60, 700, 171, 32))
        self.btn_save_file.setObjectName("btn_save_file")
        self.file_name = QtWidgets.QLineEdit(MainWindow)
        self.file_name.setGeometry(QtCore.QRect(170, 670, 113, 21))
        self.file_name.setObjectName("file_name")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(80, 670, 60, 16))
        self.label.setObjectName("label")
        self.btn_save_image = QtWidgets.QPushButton(MainWindow)
        self.btn_save_image.setGeometry(QtCore.QRect(60, 730, 171, 32))
        self.btn_save_image.setObjectName("btn_save_image")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_load_2.setText(_translate("MainWindow", "Programming Modes"))
        self.radio_echo.setText(_translate("MainWindow", "Echo Separation"))
        self.radio_machine_learning.setText(_translate("MainWindow", "Machine Learning Mode"))
        self.label_load.setText(_translate("MainWindow", "Select File"))
        self.btn_load_file.setText(_translate("MainWindow", "Load Files"))
        item = self.table_widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Folder"))
        item = self.table_widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "File"))
        self.btn_start_echo.setText(_translate("MainWindow", "Start Echo Mode"))
        self.btn_save_file.setText(_translate("MainWindow", "Save Result File"))
        self.label.setText(_translate("MainWindow", "File Name"))
        self.btn_save_image.setText(_translate("MainWindow", "Save Result Image"))

