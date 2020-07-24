import sqlite3

types_q = '''CREATE TABLE IF NOT EXISTS event_types (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE,
                                        type TEXT
                                    ); '''
event_q = '''CREATE TABLE IF NOT EXISTS events (
                                    id integer PRIMARY KEY,
                                    type_id integer, 
                                    time integer, 
                                    data text, 
                                    notes text, 
                                    created_time integer, 
                                    FOREIGN KEY (type_id) REFERENCES event_types (id)
                                );'''
db = sqlite3.connect('data/test.db')
cursor = db.cursor()
cursor.execute(types_q)
cursor.execute(event_q)
print('Data tables created. ')