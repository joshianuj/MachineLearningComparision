from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import glob
import operator

from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy, QScrollArea
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView, QVBoxLayout, QHeaderView
from glob import glob
from os.path import basename
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random

from utils import data_processing
from ui_files import MainWindow
import pandas as pd

class MainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Setup Operations
        self.btn_load_file.pressed.connect(self.load_file)
        self.btn_start_echo.pressed.connect(self.start_echo_separation)
        self.btn_save_file.pressed.connect(self.save_to_file)
        self.btn_save_image.pressed.connect(self.save_to_image)
        self.files = None

        self.overall_echos = []

        self.show()
  
    def load_file(self):
        directory = str(QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        paths = glob(f'{directory}/*')
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

    def make_echo_chart(self, echos_data):
        qscrollContents = QWidget()
        qscrollLayout = QVBoxLayout(qscrollContents)
        self.scrollAreaWidget = qscrollLayout
        self.scrollAreaEcho.setWidget(qscrollContents)
        qfigWidget = QWidget(qscrollContents)
        fig = Figure((13.0, 13.0))
        canvas = FigureCanvas(fig)
        canvas.setParent(qfigWidget)
        toolbar = NavigationToolbar(canvas, qfigWidget)
        counter = 0
        for index, echo_data in enumerate(echos_data):
            if counter < 20:
                counter +=1
                axes = fig.add_subplot(5,5, counter)
                axes.plot(echo_data)
        plotLayout = QVBoxLayout()
        plotLayout.addWidget(canvas)
        plotLayout.addWidget(toolbar)
        qfigWidget.setLayout(plotLayout)

        # prevent the canvas to shrink beyond a point
        # original size looks like a good minimum size
        qscrollLayout.addWidget(qfigWidget)
        qscrollContents.setLayout(qscrollLayout)
  
    def start_echo_separation(self):
        qscrollContents = QWidget()
        qscrollLayout = QVBoxLayout(qscrollContents)
        self.scrollAreaWidget = qscrollLayout
        self.scrollArea.setWidget(qscrollContents)
        self.overall_echos = []
        for file_name in self.files:
            time_domain_data_set = data_processing.get_time_domain_without_offset(file_name['absolute_path'])
            # lowpassfilterdata =  data_processing.use_low_pass_filter(time_domain_data_set)
            echos_data, cut_index_list =  data_processing.get_echos(time_domain_data_set)
            self.overall_echos.append(echos_data)
            qfigWidget = QWidget(qscrollContents)
            fig = Figure((10.0, 10.0))
            canvas = FigureCanvas(fig)
            canvas.setParent(qfigWidget)
            toolbar = NavigationToolbar(canvas, qfigWidget)
            axes = fig.add_subplot(2,2, 1)
            axes.plot(time_domain_data_set[0])
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
    
    # def start_echo_separation(self):
    #     qscrollContents = QWidget()
    #     qscrollLayout = QVBoxLayout(qscrollContents)
    #     self.scrollAreaWidget = qscrollLayout
    #     self.scrollArea.setWidget(qscrollContents)
    #     self.overall_echos = []
    #     for file_name in self.files:
    #         time_domain_data_set = data_processing.get_time_domain_without_offset(file_name['absolute_path'])
    #         # lowpassfilterdata =  data_processing.use_low_pass_filter(time_domain_data_set)
    #         echos_data, cut_index_list =  data_processing.get_echos(time_domain_data_set)
    #         self.overall_echos.append(echos_data)
    #         echo_index = 0
    #         for index, time_domain_data in enumerate(time_domain_data_set):
    #             qfigWidget = QWidget(qscrollContents)

    #             fig = Figure((5.0, 5.0))
    #             canvas = FigureCanvas(fig)
    #             canvas.setParent(qfigWidget)
    #             toolbar = NavigationToolbar(canvas, qfigWidget)
    #             axes = fig.add_subplot(221)
    #             axes.plot(time_domain_data)
    #             if index not in cut_index_list:
    #                 axes = fig.add_subplot(222)
    #                 axes.plot(echos_data[echo_index])
    #                 echo_index += 1

    #             # place plot components in a layout
    #             plotLayout = QVBoxLayout()
    #             plotLayout.addWidget(canvas)
    #             plotLayout.addWidget(toolbar)
    #             qfigWidget.setLayout(plotLayout)

    #             # prevent the canvas to shrink beyond a point
    #             # original size looks like a good minimum size
    #             canvas.setMinimumSize(canvas.size())
    #             qscrollLayout.addWidget(qfigWidget)
    #     qscrollContents.setLayout(qscrollLayout)

    def save_to_file(self):
        print('here')
        df = pd.DataFrame(self.overall_echos)
        df.to_csv(f'../../data/Result/{self.file_name.text()}.csv', header=False, index=False)

    def save_to_image(self):
        print('here')
        widget = self.scrollArea.widget()
        pixmap = QPixmap(widget.size())
        widget.render(pixmap)
        pixmap.save('filename.png', 'PNG')


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Data Analysis")

    window = MainWindow()
    app.exec_()