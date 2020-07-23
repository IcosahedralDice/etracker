import sqlite3
from datetime import datetime

def retrieve_events(match: str=''):
    conn = sqlite3.connect('data/test.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT time, name, data, notes from events LEFT JOIN event_types''')
    return [(datetime.fromtimestamp(x[0]).strftime('%d %b %y %H:%M:%S'), x[1], x[2], x[3]) for x in cursor.fetchall()
            if match in x[1]]