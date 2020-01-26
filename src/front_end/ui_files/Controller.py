# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Controller.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ControllerWindow(object):
    def setupUi(self, ControllerWindow):
        ControllerWindow.setObjectName("ControllerWindow")
        ControllerWindow.resize(1600, 1200)
        self.centralwidget = QtWidgets.QWidget(ControllerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.radio_data_processing = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_data_processing.setGeometry(QtCore.QRect(690, 250, 481, 20))
        self.radio_data_processing.setObjectName("radio_data_processing")
        self.radio_ml_training = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_ml_training.setGeometry(QtCore.QRect(690, 280, 481, 20))
        self.radio_ml_training.setObjectName("radio_ml_training")
        self.radio_ml_predict = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_ml_predict.setGeometry(QtCore.QRect(690, 310, 481, 20))
        self.radio_ml_predict.setObjectName("radio_ml_predict")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(680, 360, 113, 32))
        self.btn_open.setObjectName("btn_open")
        ControllerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ControllerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 22))
        self.menubar.setObjectName("menubar")
        ControllerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ControllerWindow)
        self.statusbar.setObjectName("statusbar")
        ControllerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ControllerWindow)
        QtCore.QMetaObject.connectSlotsByName(ControllerWindow)

    def retranslateUi(self, ControllerWindow):
        _translate = QtCore.QCoreApplication.translate
        ControllerWindow.setWindowTitle(_translate("ControllerWindow", "MainWindow"))
        self.radio_data_processing.setText(_translate("ControllerWindow", "Data Processing"))
        self.radio_ml_training.setText(_translate("ControllerWindow", "Machine Learning Training"))
        self.radio_ml_predict.setText(_translate("ControllerWindow", "Machine Learning Prediction"))
        self.btn_open.setText(_translate("ControllerWindow", "Open UI"))

