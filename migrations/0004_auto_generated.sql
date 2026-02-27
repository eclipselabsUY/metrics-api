-- upgrade

CREATE TABLE IF NOT EXISTS events (
    id INTEGER NOT NULL PRIMARY KEY,
    event_type_id INTEGER NOT NULL REFERENCES event_types(id),
    timestamp DATETIME,
    client_ip VARCHAR(45),
    event_metadata JSON,
    service_id INTEGER NOT NULL REFERENCES services(id)
)

CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER NOT NULL PRIMARY KEY,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    prefix VARCHAR(32) NOT NULL,
    service_id INTEGER NOT NULL REFERENCES services(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
)

-- rollback

DROP TABLE api_keys

DROP TABLE events
