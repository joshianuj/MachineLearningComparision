import sys
import os
from glob import glob
from os.path import basename
import pickle

from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView, QVBoxLayout, QHeaderView


class Widget(QWidget):
    
    def __init__(self):
        super().__init__()
        uifile = os.path.join(os.path.dirname(__file__), '../front_end/DataAnalysis.ui')
        self.ui = loadUi(uifile, self)

        for elem in self.ui.children():
            name = elem.objectName()
            
            if name == 'files_frame':
                for child_elem in elem.children():
                    child_name = child_elem.objectName()
                    
                    if child_name == 'btn_load_file':
                        child_elem.clicked.connect(self.load_file)
                    elif child_name == 'table_widget':
                        self.table = child_elem
                    elif child_name == 'btn_start_echo':
                        child_elem.clicked.connect(self.start_echo_separation)
            elif name == 'mode_frame':
                for child_elem in elem.children():
                    child_name = child_elem.objectName()

                    if child_name == 'radio_echo':
                        child_elem.clicked.connect(self.echo_separation)
                    elif child_name == 'radio_machine_learning':
                        child_elem.clicked.connect(self.machine_learning)
            elif name == 'ai_frame': 
               print('hello')

    def echo_separation(self):
        print('echo separation')
    
    def machine_learning(self):
        print('machine learning')

    def load_file(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        paths = glob(f'{directory}/*')
        files = []
        if len(paths) > 0:
            for p in paths:
                files += glob(f'{p}/*.csv')
        self.load_files_in_table(files)

    def load_files_in_table(self, files):
        self.table.setRowCount(len(files))
        for row, item in enumerate(files):
            self.table.setItem(row, 0, QTableWidgetItem(item.split('/')[-2]))
            self.table.setItem(row, 1, QTableWidgetItem(basename(item)))

    def start_echo_separation(self):
        print('clicked this method')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())


