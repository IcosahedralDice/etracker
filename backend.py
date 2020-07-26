import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/test.db')


def retrieve_events(match: str = '', limit: int = 100):
    cursor = conn.cursor()
    cursor.execute(
        f'''SELECT time, name, data, notes, events.id from events INNER JOIN event_types on events.type_id = event_types.id 
        WHERE name LIKE '%{match}%' or notes like '%{match}%' ORDER BY time DESC LIMIT {limit}''')
    x = [(datetime.fromtimestamp(x[0]).strftime('%d %b %y %H:%M'), x[1], x[2], x[3], x[4]) for x in cursor.fetchall()]
    return x


def retrieve_event_types(match: str = ''):
    cursor = conn.cursor()
    cursor.execute(f'''
        select distinct name, type, event_types.id from event_types
        join (select * from events order by id desc) where type_id = event_types.id and name like '%{match}%';''')
    return [(x[1], x[0], x[2]) for x in cursor.fetchall()]


def event_type_info(id: int):
    cursor = conn.cursor()
    cursor.execute(f'select distinct name, type from event_types where id = {id};')
    x = cursor.fetchall()
    return x[0][0], x[0][1]


def new_event(type_id: int, time: int, notes: str, data: str = None):
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO events (type_id, time, data, notes, created_time) VALUES (?, ?, ?, ?, ?)',
                   (type_id, time, data, notes, int(datetime.now().timestamp())))
    conn.commit()


def new_event_type(name: str, type: str):
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO event_types (name, type) VALUES (?, ?)', (name, type))
    row = cursor.lastrowid
    now = int(datetime.now().timestamp())
    cursor.execute(f'INSERT INTO events (type_id, time, notes, created_time) VALUES (?, ?, ?, ?)',
                   (row, now, 'Created', now))
    conn.commit()
