-- upgrade

CREATE TABLE IF NOT EXISTS event_types (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    service_id INTEGER NOT NULL REFERENCES services(id)
)

-- rollback

DROP TABLE event_types
