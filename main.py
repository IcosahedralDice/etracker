from PyQt5 import QtWidgets, uic
import sys  # We need sys so that we can pass argv to QApplication
import backend
from datetime import datetime

from PyQt5.QtWidgets import *

max_rows = 40


def reload_page(table: QtWidgets.QTableWidget, data):
    start = datetime.now()
    for i in range(min(max_rows, len(data))):
        for j in range(len(data[i])):
            table.item(i, j).setText(data[i][j])
    for i in range(min(max_rows, len(data)), max_rows):
        for j in range(4):
            table.item(i, j).setText('')
    end = datetime.now()
    print('reload_page: ', end - start)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('MainWindow.ui', self)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.setRowCount(max_rows)
        ohead = self.tableWidget.verticalHeader()
        for i in range(max_rows):
            ohead.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(''))

        self.searchBar.textEdited.connect(
            lambda x: reload_page(self.tableWidget, backend.retrieve_events(x, limit=max_rows)))

        reload_page(self.tableWidget, backend.retrieve_events())


app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
