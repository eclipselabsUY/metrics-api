-- upgrade

CREATE TABLE IF NOT EXISTS events (
    id INTEGER NOT NULL PRIMARY KEY,
    event_type_id INTEGER NOT NULL REFERENCES event_types(id),
    timestamp DATETIME,
    client_ip VARCHAR(45),
    event_metadata JSON
)

CREATE TABLE IF NOT EXISTS services (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50),
    url VARCHAR(150),
    service_type_id INTEGER NOT NULL REFERENCES service_types(id)
)

CREATE TABLE IF NOT EXISTS service_types (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    kind VARCHAR(8) NOT NULL
)

CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER NOT NULL PRIMARY KEY,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    service_id INTEGER NOT NULL REFERENCES services(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
)

CREATE TABLE IF NOT EXISTS event_types (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
)

-- rollback

DROP TABLE event_types

DROP TABLE api_keys

DROP TABLE service_types

DROP TABLE services

DROP TABLE events
