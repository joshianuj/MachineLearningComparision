from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import glob
import operator

from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy, QScrollArea, QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView, QVBoxLayout, QHeaderView
from glob import glob
from os.path import basename
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random

from utils import data_processing, feature_extraction
from ui_files import MainWindow
from filter import DataProcessor
import pandas as pd
from utils.plot_canvas import PlotCanvas

import numpy as np


class DataProcessingWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, channel, *args, **kwargs):
        super(DataProcessingWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.channel = channel

        # Setup Operations
        self.btn_load_file.pressed.connect(self.load_file)
        self.btn_save_echo.pressed.connect(self.save_echo_to_file)
        self.files = None
        self.overall_echos = []

        # assign data_processing
        self.data_processing = DataProcessor()

        # parameter_frame
        # self.echo_size.textChanged.connect(self.update_echo_size)
        # self.noise_size.textChanged.connect(self.update_noise_size)
        self.plot_index.currentTextChanged.connect(
            self.add_plots)
        self.sample_frequency.currentTextChanged.connect(
            self.on_combobox_changed)

        # canvas
        self.echo_plot = PlotCanvas(self, width=5, height=5, dpi=70, title="Echo data")
        self.echo_box.addWidget(self.echo_plot)

        self.time_domain_plot = PlotCanvas(
            self, width=5, height=5, dpi=70, title="Time Domain data")
        self.signal_box.addWidget(self.time_domain_plot)

        self.fft_plot = PlotCanvas(
            self, width=5, height=5, dpi=75, title="FFT data")
        self.fft_box.addWidget(self.fft_plot)

        self.btn_data_open.setEnabled(False)
        self.btn_ml_open.pressed.connect(self.channel.open_ml_window)
        self.btn_ml_prediction_open.pressed.connect(
            self.channel.open_ml_prediction_window)

        # self.show()

    def set_controller(self, controller):
        self.controller = controller

    def on_combobox_changed(self, value):
        self.data_processing.change_selected_element(value)
        self.echo_size.setText(str(self.data_processing.ECHO_SIZE))
        self.noise_size.setText(str(self.data_processing.NOISE_SIZE))

    def error_dailog(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def update_echo_size(self, value):
        try:
            self.data_processing.ECHO_SIZE_LEFT = int(value)
        except:
            self.error_dailog('Value Should not have String')

    def update_noise_size(self, value):
        try:
            self.data_processing.ECHO_SIZE_LEFT = int(value)
        except:
            self.error_dailog('Value Should not have String')

    def load_file(self):
        try:
            directory = str(QFileDialog.getExistingDirectory(
                self, "Select Directory"))
            paths = glob(f'{directory}/*/*')
            files = []
            if len(paths) > 0:
                for p in paths:
                    files += glob(f'{p}/*.csv')
            if not files:
                files = paths
            new_files_set = []
            for item in files:
                new_files_set.append({
                    'folder_name': int(item.split('/')[-2]),
                    'file_name': basename(item),
                    'absolute_path': item,
                    'type': item.split('/')[-4].upper(),
                    'model': item.split('/')[-3],
                })
            self.load_files_in_table(
                sorted(new_files_set, key=lambda i: i['folder_name']))
        except:
            self.error_dailog('Please choose a file')

    def load_files_in_table(self, files):
        self.files = files
        self.table_widget.setRowCount(len(files))
        for row, item in enumerate(files):
            self.table_widget.setItem(
                row, 0, QTableWidgetItem(str(item['type'])))
            self.table_widget.setItem(
                row, 1, QTableWidgetItem(item['file_name']))
            self.table_widget.setItem(
                row, 2, QTableWidgetItem(item['model']))
            btn = QPushButton(f'Plot')
            btn.objectName = str(row)
            btn.clicked.connect(self.make_chart_with_file_index)
            self.table_widget.setCellWidget(row, 3, btn)

    def make_chart_with_file_index(self, file_name):
        try:
            import re
            # index = int(re.search(r'\d+', self.sender().text()).group())
            index = int(re.search(r'\d+', self.sender().objectName).group())

            self.time_domain_data_set = self.data_processing.get_time_domain_without_offset(
                self.files[index]['absolute_path'])

            self.plot_index.clear()
            for i in range(self.time_domain_data_set.shape[0]):
                self.plot_index.addItem(str(i))

        except:
            self.error_dailog('Chart cannot be created')

    def add_plots(self, value):
        try:
            if value:
                index = int(value)
                filtered_data_values = self.data_processing.get_filtered_values(
                    self.time_domain_data_set)
                echos_data = self.data_processing.get_echo_with_index(
                    filtered_data_values[index])
                self.time_domain_plot.plot(filtered_data_values[index])
                if echos_data:
                    self.echo_plot.plot(echos_data[0]['ECHO'])
                    x, y = feature_extraction.fft_chart_value(
                        np.array(echos_data[0]['ECHO']), self.data_processing.selected_element['value'])
                    self.fft_plot.plot_x_y(x, y)
                else:
                    self.echo_plot.plot([])
        except:
            self.error_dailog('Combobox not ready, please Plot first')

    def get_features_from_echo(self, echos_data, row):
        df_fft = echos_data.iloc[:, 1:]
        fft_list = feature_extraction.fft_from_data_frame(
            df_fft, self.data_processing.selected_element['value'])
        fft_set = pd.DataFrame(fft_list)

        fft_set['model'] = row['model']
        fft_set['type'] = row['type']
        fft_set['distance'] = row['distance']
        fft_set = fft_set.set_index(
            ['distance', 'type', 'model']).reset_index()
        return fft_set

    def save_echo_to_file(self):
        echo_data_set = pd.DataFrame()
        fft_data_set = pd.DataFrame()
        for index, file in enumerate(self.files):
            if len(file['absolute_path'].split('/')) >= 4:
                time_domain_data_set = self.data_processing.get_time_domain_without_offset(
                    file['absolute_path'])
                filtered_data_values = self.data_processing.get_filtered_values(
                    time_domain_data_set)
                echos_data = self.data_processing.find_echos(
                    filtered_data_values)
                if isinstance(echos_data, pd.DataFrame):
                    row = {
                        'type': file['absolute_path'].split('/')[-4].upper(),
                        'model': file['absolute_path'].split('/')[-3],
                        'distance': file['folder_name']
                    }
                    fft_data_set = fft_data_set.append(
                        self.get_features_from_echo(echos_data, row), ignore_index=True)

                    echos_data['model'] = row['model']
                    echos_data['type'] = row['type']
                    echos_data['distance'] = row['distance']
                    echos_data = echos_data.set_index(
                        ['distance', 'type', 'model']).reset_index()
                    echo_data_set = echo_data_set.append(
                        echos_data, ignore_index=True)
        if self.echo_file_name.text():
            echo_data_set.to_csv(
                f"{self.data_processing.selected_element['echo']}{self.echo_file_name.text()}.csv")
            fft_data_set.to_csv(
                f"{self.data_processing.selected_element['features']}{self.echo_file_name.text()}.csv")

    @pyqtSlot()
    def open_ml_window(self):
        self.machine_learning_window.show()
        self.close()

    @pyqtSlot()
    def open_ml_prediction_window(self):
        self.machine_learning_prediction_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Data Analysis")

    window = DataProcessingWindow()
    app.exec_()
