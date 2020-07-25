from PyQt5 import QtWidgets, uic
import sys  # We need sys so that we can pass argv to QApplication
import backend
from datetime import datetime

from PyQt5.QtWidgets import *

max_rows = 1000


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        self.displaying_events = True

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
            lambda x: self.reload_page(self.tableWidget, x))
        self.addButton.clicked.connect(
            lambda x: self.change_table_display(self.addButton))

        self.reload_page(self.tableWidget)

    def change_table_display(self, button: QtWidgets.QPushButton):
        self.displaying_events = not self.displaying_events
        button.setText('Types' if self.displaying_events else 'Events')
        self.reload_page(self.tableWidget)

    def reload_page(self, table: QtWidgets.QTableWidget, match: str = ''):
        if self.displaying_events:
            table.setUpdatesEnabled(False)
            data = backend.retrieve_events(limit=max_rows, match=match)

            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(['Time', 'Event', 'Data', 'Notes'])
            table.setRowCount(min(max_rows, len(data)))

            for i in range(min(max_rows, len(data))):
                for j in range(len(data[i])):
                    table.setItem(i, j, QTableWidgetItem(data[i][j]))
            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
            table.setUpdatesEnabled(True)
        else:
            data = backend.retrieve_event_types(match=match)

            table.setUpdatesEnabled(False)
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(['Type', 'Name'])
            table.setRowCount(len(data))

            for i in range(len(data)):
                table.setItem(i, 0, QTableWidgetItem(data[i][0]))
                table.setItem(i, 1, QTableWidgetItem(data[i][1]))
            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            table.setUpdatesEnabled(True)


app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
