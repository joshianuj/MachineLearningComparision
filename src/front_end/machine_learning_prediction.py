from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import glob
import operator
from sklearn.model_selection import train_test_split
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy, QScrollArea, QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView, QVBoxLayout, QHeaderView
from glob import glob
from os.path import basename
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random

from utils import data_processing, feature_extraction, normalize
from machine_learning import MachineLearningHelper
import pandas as pd
from utils.plot_canvas import PlotCanvas
from ui_files import MachineLearningPrediction

import numpy as np
import pickle
from collections import Counter


class MachineLearningPredictionWindow(QMainWindow, MachineLearningPrediction.Ui_MachineLearningPrediction):

    def __init__(self, channel, *args, **kwargs):
        super(MachineLearningPredictionWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Setup Operations
        self.btn_load_file.pressed.connect(self.load_file)
        self.channel = channel
        self.files = None
        self.data_set = {}
        # assign data_processing
        self.machine_learning_processor = MachineLearningHelper()

        # canvas
        self.prediction_plot_canvas = PlotCanvas(
            self, width=2, height=2, dpi=50, title="Predicted Result")
        self.plot_prediction.addWidget(self.prediction_plot_canvas)

        self.prediction_confusion_matrix_canvas = PlotCanvas(
            self, width=2, height=2, dpi=70, title="Predicted Confusion Matrix")
        self.plot_confusion_matrix.addWidget(
            self.prediction_confusion_matrix_canvas)

        # self.btn_load_file.pressed.connect(self.start_process)
        self.btn_start_prediction.pressed.connect(
            self.on_start_prediction_press)
        self.btn_load_model.pressed.connect(self.select_model)

        self.btn_load_result_file.pressed.connect(self.load_and_plot_result)

        self.btn_ml_prediction_open.setEnabled(False)
        self.btn_ml_open.pressed.connect(self.channel.open_ml_window)
        self.btn_data_open.pressed.connect(
            self.channel.open_data_window)

    def on_start_prediction_press(self):
        if self.data_set:
            X_predict = self.data_set['all_data']['data']
            X_normalized_predict = normalize.custom_normalization(X_predict)
            result = self.machine_learning_processor.loaded_predict(
                X_normalized_predict)
            self.prediction_plot_canvas.plot_prediction(result)
            labels = [*Counter(result).keys()]  # equals to list(set(words))
            values = [*Counter(result).values()]
            counter = 1
            self.table_widget.setRowCount(3)
            for index, item in enumerate(labels):
                self.table_widget.setItem(
                    counter, 0, QTableWidgetItem(item))
                self.table_widget.setItem(
                    counter, 1, QTableWidgetItem(str(values[index])))
                counter = counter + 1
            self.predicted_result = result
        else:
            self.error_dailog('Please select training files')

    def error_dailog(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def success_dialog(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def select_model(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Open File')
            model = pickle.load(open(filename[0], 'rb'))
            self.machine_learning_processor.load_model(model)
            self.txt_model_name.setText(filename[0])
        except:
            self.error_dailog(
                'Invalid model file')

    def load_and_plot_result(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Open File')
            data = pd.read_csv(filename[0])
            if 'type' in data.columns:
                result = data.type.values.tolist()
                self.prediction_confusion_matrix_canvas.plot_confusion_matrix(
                    self.predicted_result, result)
                self.txt_model_name.setText(filename[0])
            else:
                self.error_dailog(
                    'Invalid file')
        except:
            self.error_dailog(
                'Invalid model file')

    def load_file(self):
        try:
            files = QFileDialog.getOpenFileNames(
                self, 'Open File', 'csv')
            self.data_set = {}

            for f in files[0]:
                data = pd.read_csv(f)
                if 'type' in data.columns:
                    d = data.iloc[:, 4:]
                else:
                    d = data.iloc[:, :]
                if 'all_data' not in self.data_set:
                    self.data_set['all_data'] = {}
                    self.data_set['all_data']['data'] = d.values.tolist()
                else:
                    self.data_set['all_data']['data'] = self.data_set['all_data']['data'] + \
                        d.values.tolist()
            self.load_files_in_table()
        except:
            self.error_dailog('Please choose a file')

    def load_files_in_table(self):
        files = []
        for item in self.data_set:
            files.append({
                'name': item,
                'data_size': len(self.data_set[item]['data']),
            })
        self.table_widget.setRowCount(len(files))
        for row, item in enumerate(files):
            self.table_widget.setItem(
                row, 0, QTableWidgetItem(item['name']))
            self.table_widget.setItem(
                row, 1, QTableWidgetItem(str(item['data_size'])))

    @pyqtSlot()
    def open_ml_window(self):
        self.machine_learning_window.show()
        self.close()

    @pyqtSlot()
    def open_data_window(self):
        self.data_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Machine Learning Prediction")

    window = MachineLearningPredictionWindow()
    window.show()
    app.exec_()
