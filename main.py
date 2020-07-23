from PyQt5 import QtWidgets, uic
import sys  # We need sys so that we can pass argv to QApplication
import backend

from PyQt5.QtWidgets import *


def reload_page(table: QtWidgets.QTableWidget, data):
    table.setRowCount(len(data))
    for i in range(len(data)):
        for j in range(len(data[i])):
            table.setItem(i, j, QTableWidgetItem(str(data[i][j])))
    header = table.verticalHeader()
    for i in range(len(data)):
        header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)


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

        self.searchBar.textEdited.connect(lambda x: reload_page(self.tableWidget, backend.retrieve_events(x)))

        reload_page(self.tableWidget, backend.retrieve_events())


app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
