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
        self.load_files_in_table(files)

    def load_files_in_table(self, files):
        self.files = files
        self.table_widget.setRowCount(len(files))
        for row, item in enumerate(files):
            self.table_widget.setItem(row, 0, QTableWidgetItem(item.split('/')[-2]))
            self.table_widget.setItem(row, 1, QTableWidgetItem(basename(item)))
    
    def start_echo_separation(self):
        qscrollContents = QWidget()
        qscrollLayout = QVBoxLayout(qscrollContents)
        self.scrollArea.setWidget(qscrollContents)
        self.overall_echos = []
        for file_name in self.files:
            time_domain_data_set = data_processing.get_time_domain_without_offset(file_name)
            # lowpassfilterdata =  data_processing.use_low_pass_filter(time_domain_data_set)
            echos_data, cut_index_list =  data_processing.get_echos(time_domain_data_set)
            self.overall_echos.append(echos_data)
            echo_index = 0
            for index, time_domain_data in enumerate(time_domain_data_set):
                qfigWidget = QWidget(qscrollContents)

                fig = Figure((5.0, 5.0))
                canvas = FigureCanvas(fig)
                canvas.setParent(qfigWidget)
                toolbar = NavigationToolbar(canvas, qfigWidget)
                axes = fig.add_subplot(221)
                axes.plot(time_domain_data)
                if index not in cut_index_list:
                    axes = fig.add_subplot(222)
                    axes.plot(echos_data[echo_index])
                    echo_index += 1

                # place plot components in a layout
                plotLayout = QVBoxLayout()
                plotLayout.addWidget(canvas)
                plotLayout.addWidget(toolbar)
                qfigWidget.setLayout(plotLayout)

                # prevent the canvas to shrink beyond a point
                # original size looks like a good minimum size
                canvas.setMinimumSize(canvas.size())
                qscrollLayout.addWidget(qfigWidget)
        qscrollContents.setLayout(qscrollLayout)
        self.scroll_something = qscrollContents

    def save_to_file(self):
        print('here')
        df = pd.DataFrame(self.overall_echos)
        df.to_csv(f'../../data/Result/{self.file_name.text()}.csv', header=False, index=False)

    def save_to_image(self):
        print('here')
        # pixmap = QPixmap(self.scroll_something.size())
        # self.scroll_something.render(pixmap)
        # pixmap.save('filename', 'PNG', 100)


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Data Analysis")

    window = MainWindow()
    app.exec_()