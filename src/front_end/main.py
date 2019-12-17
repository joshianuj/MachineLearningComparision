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

from utils import data_processing
from ui_files import MainWindow
from filter import DataProcessor
import pandas as pd

class MainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Setup Operations
        self.btn_load_file.pressed.connect(self.load_file)
        self.btn_save_echo.pressed.connect(self.save_echo_to_file)
        self.files = None
        self.overall_echos = []

        # assign data_processing
        self.data_processing = DataProcessor()

        # parameter_frame
        self.echo_size.textChanged.connect(self.update_echo_size)
        self.noise_size.textChanged.connect(self.update_noise_size)
        self.sample_frequency.currentTextChanged.connect(self.on_combobox_changed)

        # show UI
        self.show()

    def on_combobox_changed(self, value):
        self.data_processing.change_selected_element(value)

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
        directory = str(QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        paths = glob(f'{directory}/*/*')
        files = []
        if len(paths) > 0:
            for p in paths:
                files +=glob(f'{p}/*.csv')
        if not files:
            files = paths
        new_files_set = []
        for item in files:
            new_files_set.append({
                'folder_name': int(item.split('/')[-2]),
                'file_name': basename(item),
                'absolute_path': item
            })
        self.load_files_in_table(sorted(new_files_set, key = lambda i: i['folder_name']))

    def load_files_in_table(self, files):
        self.files = files
        self.table_widget.setRowCount(len(files))
        for row, item in enumerate(files):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(item['folder_name'])))
            self.table_widget.setItem(row, 1, QTableWidgetItem(item['file_name']))
            btn = QPushButton(f'Plot:{row}')
            btn.clicked.connect(self.make_chart_with_file_index)
            self.table_widget.setCellWidget(row, 2, btn)

    def make_chart_with_file_index(self, file_name):
        import re
        index = int(re.search(r'\d+', self.sender().text()).group())
        qscrollContents = QWidget()
        qscrollLayout = QVBoxLayout(qscrollContents)
        self.scrollAreaWidget = qscrollLayout
        self.scrollArea.setWidget(qscrollContents)
        
        time_domain_data_set = self.data_processing.get_time_domain_without_offset(self.files[index]['absolute_path'])
        filtered_data =  self.data_processing.get_filtered_values(time_domain_data_set)
        echos_data =  self.data_processing.get_echos(filtered_data)

        qfigWidget = QWidget(qscrollContents)
        fig = Figure((10.0, 10.0))
        canvas = FigureCanvas(fig)
        canvas.setParent(qfigWidget)
        toolbar = NavigationToolbar(canvas, qfigWidget)
        axes = fig.add_subplot(2,2, 1)
        axes.plot(time_domain_data_set.values[0])
        axes = fig.add_subplot(2,2, 2)
        axes.plot(echos_data[0])

        # place plot components in a layout
        plotLayout = QVBoxLayout()
        plotLayout.addWidget(canvas)
        plotLayout.addWidget(toolbar)
        qfigWidget.setLayout(plotLayout)

        # prevent the canvas to shrink beyond a point
        # original size looks like a good minimum size
        # canvas.setMinimumSize(canvas.size())
        qscrollLayout.addWidget(qfigWidget)
        qscrollContents.setLayout(qscrollLayout)
  
    def save_echo_to_file(self):
        echo_data_set = pd.DataFrame()
        for index, file in enumerate(self.files):
            if len(file['absolute_path'].split('/')) >= 4:
                time_domain_data_set = self.data_processing.get_time_domain_without_offset(file['absolute_path'])
                filtered_data =  self.data_processing.get_filtered_values(time_domain_data_set)
                echos_data =  self.data_processing.get_echos(filtered_data)
                row = {
                    'type': file['absolute_path'].split('/')[-4],
                    'model': file['absolute_path'].split('/')[-3],
                    'distance': file['folder_name']
                }
                df = pd.DataFrame(echos_data)
                len_of_echo = len(echos_data)
                df['model'] = [file['absolute_path'].split('/')[-3]]*len_of_echo
                df['type'] = [file['absolute_path'].split('/')[-4]]*len_of_echo
                df['distance'] = [file['folder_name']]*len_of_echo
                df = df.set_index(['distance', 'type', 'model']).reset_index()
                echo_data_set = echo_data_set.append(df, ignore_index = True)
        if self.echo_file_name.text():
            echo_data_set.to_csv(f'./data/result/{self.echo_file_name.text()}.csv')


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Data Analysis")

    window = MainWindow()
    app.exec_()