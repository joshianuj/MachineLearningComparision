from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy, QScrollArea, QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView, QVBoxLayout, QHeaderView

from ui_files import Controller

from machine_learning_training import MachineLearningWindow
from machine_learning_prediction import MachineLearningPredictionWindow
from data_processing_window import DataProcessingWindow

import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ControllerWindow(QMainWindow, Controller.Ui_ControllerWindow):
    def __init__(self, *args, **kwargs):
        super(ControllerWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.btn_open.pressed.connect(self.open_window)

        self.data_window = DataProcessingWindow(self)
        self.machine_learning_window = MachineLearningWindow(self)
        self.machine_learning_prediction_window = MachineLearningPredictionWindow(
            self)
        # show UI
        self.show()

    def error_dailog(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    @pyqtSlot()
    def open_window(self):
        if self.radio_data_processing.isChecked():
            self.data_window.show()
        elif self.radio_ml_training.isChecked():
            self.machine_learning_window.show()
        elif self.radio_ml_predict.isChecked():
            self.machine_learning_prediction_window.show()
        else:
            self.error_dailog('Please select an option')
            return
        self.close()

    @pyqtSlot()
    def open_ml_prediction_window(self):
        self.machine_learning_prediction_window.show()
        self.machine_learning_window.hide()
        self.data_window.hide()
        self.close()

    @pyqtSlot()
    def open_ml_window(self):
        self.machine_learning_window.show()
        self.machine_learning_prediction_window.hide()
        self.data_window.hide()
        self.close()

    @pyqtSlot()
    def open_data_window(self):
        self.data_window.show()
        self.machine_learning_window.hide()
        self.machine_learning_prediction_window.hide()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Machine Learning")

    window = ControllerWindow()
    app.exec_()
