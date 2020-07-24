import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/test.db')


def retrieve_events(match: str = '', limit: int = 100):
    start = datetime.now()
    cursor = conn.cursor()
    cursor.execute(
        f'''SELECT time, name, data, notes from events INNER JOIN event_types on events.type_id = event_types.id 
        WHERE name LIKE '%{match}%' ORDER BY time DESC LIMIT {limit}''')
    x = [(datetime.fromtimestamp(x[0]).strftime('%d %b %y %H:%M'), x[1], x[2], x[3]) for x in cursor.fetchall()]
    end = datetime.now()
    print('retrieve_events: ', end - start)
    return x
