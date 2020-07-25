import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/test.db')


def retrieve_events(match: str = '', limit: int = 100):
    cursor = conn.cursor()
    cursor.execute(
        f'''SELECT time, name, data, notes from events INNER JOIN event_types on events.type_id = event_types.id 
        WHERE name LIKE '%{match}%' ORDER BY time DESC LIMIT {limit}''')
    x = [(datetime.fromtimestamp(x[0]).strftime('%d %b %y %H:%M'), x[1], x[2], x[3]) for x in cursor.fetchall()]
    return x


def retrieve_event_types(match: str = ''):
    cursor = conn.cursor()
    cursor.execute(f'''
        select distinct name, type from event_types
        join (select * from events order by id desc) where type_id = event_types.id and name like '%{match}%';''')
    return [(x[1], x[0]) for x in cursor.fetchall()]
