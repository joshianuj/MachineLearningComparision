from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView, QVBoxLayout, QHeaderView
from os.path import basename

class UITable(QTableWidget):
    def __init__(self, parent=None, row=5, column=3):
        QTableWidget.__init__(self, parent)
        self.table = QTableWidget(self)
        self.setParent(parent)

        self.table.setRowCount(row)
        self.table.setColumnCount(column)
        self.table.setItem(0, 0, QTableWidgetItem("File Name"))

        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def load_items(self, items):
        row = 1
        column = 0
        for item in items:
            self.table.setItem(row, column, QTableWidgetItem(basename(item)))
            row += 1


if __name__ == '__main__':
    print('table')