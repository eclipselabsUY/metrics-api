-- upgrade

CREATE TABLE event_types (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE events (
    id INTEGER NOT NULL PRIMARY KEY,
    event_type_id INTEGER NOT NULL,
    timestamp DATETIME,
    client_ip VARCHAR(45),
    event_metadata JSON,
    FOREIGN KEY (event_type_id) REFERENCES event_types (id)
);

-- rollback

DROP TABLE event_types;

DROP TABLE events;
