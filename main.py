from PyQt5 import QtWidgets, uic
import sys  # We need sys so that we can pass argv to QApplication
import backend
from datetime import datetime

from PyQt5.QtWidgets import *

max_rows = 1000


def reload_page(table: QtWidgets.QTableWidget, data):
    table.setUpdatesEnabled(False)
    table.setRowCount(min(max_rows, len(data)))
    for i in range(min(max_rows, len(data))):
        for j in range(len(data[i])):
            table.setItem(i, j, QTableWidgetItem(data[i][j]))
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
    table.setUpdatesEnabled(True)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('uifiles/MainWindow.ui', self)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.setRowCount(max_rows)
        for i in range(max_rows):
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(''))

        self.searchBar.textEdited.connect(
            lambda x: reload_page(self.tableWidget, backend.retrieve_events(x, limit=max_rows)))

        reload_page(self.tableWidget, backend.retrieve_events(limit=max_rows))


app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
