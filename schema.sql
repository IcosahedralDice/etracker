CREATE TABLE IF NOT EXISTS event_types (
    id integer PRIMARY KEY,
    name text NOT NULL UNIQUE,
    type TEXT
);
CREATE TABLE IF NOT EXISTS events (
    id integer PRIMARY KEY,
    type_id integer,
    time integer,
    data text,
    notes text,
    created_time integer,
    FOREIGN KEY (type_id) REFERENCES event_types (id)
);