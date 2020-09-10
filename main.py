from PyQt5 import QtWidgets, uic, QtCore
import sys  # We need sys so that we can pass argv to QApplication
import backend
from datetime import datetime

from PyQt5.QtWidgets import *

max_rows = 1000


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        self.displaying_events = True
        self.table_row_ids = []

        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('uifiles/MainWindow.ui', self)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget.itemClicked.connect(lambda x: self.handle_table_clicks(x))

        self.newEventType.triggered.connect(self.add_event)

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
        table.setUpdatesEnabled(False)
        if self.displaying_events:
            data = backend.retrieve_events(limit=max_rows, match=match)
            self.table_row_ids = [x[4] for x in data]
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(['Time', 'Event', 'Data', 'Notes'])
            table.setRowCount(min(max_rows, len(data)))

            for i in range(min(max_rows, len(data))):
                for j in range(4):
                    table.setItem(i, j, QTableWidgetItem(data[i][j]))
            table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        else:
            data = backend.retrieve_event_types(match=match)
            self.table_row_ids = [x[2] for x in data]
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(['Type', 'Name'])
            table.setRowCount(len(data))

            for i in range(len(data)):
                table.setItem(i, 0, QTableWidgetItem(data[i][0]))
                table.setItem(i, 1, QTableWidgetItem(data[i][1]))
            table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.countLabel.setText(f'Count: {len(data)}')
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setUpdatesEnabled(True)

    def handle_table_clicks(self, position: QtCore.QModelIndex):
        if self.displaying_events:
            # Open a window with the event
            pass
        else:
            # Open a window to add an event of that type
            name, type = backend.event_type_info(self.table_row_ids[position.row()])
            if type == 'Normal':
                dialog = uic.loadUi('uifiles/BasicEvent.ui')
                dialog.setWindowTitle(f'{name}')
                dialog.timeInput.setDateTime(datetime.now())
                result = dialog.exec()
                notes = dialog.notesInput.text()
                dt = dialog.timeInput.dateTime()
                if result:
                    backend.new_event(self.table_row_ids[position.row()], dt.toSecsSinceEpoch(), notes, None)

            elif type == 'Bool':
                dialog = uic.loadUi('uifiles/BoolEvent.ui')
                dialog.setWindowTitle(f'{name}')
                dialog.timeInput.setDateTime(datetime.now())
                result = dialog.exec()
                checked = dialog.doneCheckBox.isChecked()
                notes = dialog.notesInput.text()
                dt = dialog.timeInput.dateTime()
                if result:
                    backend.new_event(self.table_row_ids[position.row()], dt.toSecsSinceEpoch(), notes,
                                      'Done' if checked else 'Skipped')

            elif type == 'Number':
                dialog = uic.loadUi('uifiles/NumberEvent.ui')
                dialog.setWindowTitle(f'{name}')
                dialog.timeInput.setDateTime(datetime.now())
                result = dialog.exec()
                if result:
                    data = dialog.valueInput.text()
                    try:
                        value = int(data)
                        notes = dialog.notesInput.text()
                        dt = dialog.timeInput.dateTime()
                        backend.new_event(self.table_row_ids[position.row()], dt.toSecsSinceEpoch(), notes, str(value))
                    except Exception:
                        error = uic.loadUi('uifiles/ErrorWindow.ui')
                        error.setWindowTitle('Error!')
                        error.errorLabel.setText(f'{data} is not a number!')
                        error.exec()

    @staticmethod
    def add_event():
        dialog = uic.loadUi('uifiles/NewEventTypeDialog.ui')
        result = dialog.exec()
        if result:
            cursor = backend.conn.cursor()
            cursor.execute(f'''SELECT * from event_types WHERE name = '{dialog.lineEdit.text()}' ''')
            existing = cursor.fetchall()
            if len(existing) == 0:
                backend.new_event_type(dialog.lineEdit.text(), dialog.comboBox.currentText())
            else:
                error = uic.loadUi('uifiles/ErrorWindow.ui')
                error.errorLabel.setText(f'Already an event type called {dialog.lineEdit.text()}')
                error.exec()

app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
