import csv
import sqlite3
from datetime import datetime

fname = input('.csv file (make sure it is in the same directory): ')
conn = sqlite3.connect('data/test.db')
cursor = conn.cursor()

with open(fname) as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar=r'"')
    event_types = set()
    events = list()
    top = None
    processed = 0
    for row in reader:
        if top is None:
            top = row
            continue

        date = f'{row[0]} {row[1]}'
        event_type = row[2]
        if row[3] is None:
            event_type_type = 'Normal'
        elif row[3] == 'Done' or row[3] == 'Skipped':
            event_type_type = 'Bool'
        else:
            event_type_type = 'Number'
        cursor.execute('INSERT OR IGNORE INTO event_types (name, type) VALUES (?, ?)', (event_type, event_type_type))
        conn.commit()
        on = row[5]
        cursor.execute(f'SELECT id from event_types WHERE name = \'{event_type}\'')
        id = cursor.fetchall()[0][0]
        cursor.execute('INSERT INTO events (type_id, time, data, notes, created_time) VALUES (?, ?, ?, ?, ?)',
                       (id, datetime.strptime(date, '%d %b %Y %H:%M').timestamp(), row[3], row[4], datetime.strptime(on, '%d %b %Y %H:%M:%S')))
        conn.commit()

        processed += 1
        if processed % 1000 == 0:
            print(f'Processed {processed} items. ')
