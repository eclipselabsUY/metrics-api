-- upgrade

CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    prefix VARCHAR(32) NOT NULL,
    service_id INTEGER NOT NULL REFERENCES services(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
)

CREATE TABLE IF NOT EXISTS rate_limit_configs (
    id SERIAL PRIMARY KEY,
    service_id INTEGER NOT NULL REFERENCES services(id),
    endpoint_pattern VARCHAR(255) NOT NULL DEFAULT '/',
    max_requests INTEGER NOT NULL DEFAULT 1000,
    window_seconds INTEGER NOT NULL DEFAULT 3600
)

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_type_id INTEGER NOT NULL REFERENCES event_types(id),
    timestamp TIMESTAMP,
    client_ip VARCHAR(45),
    event_metadata JSON
)

-- rollback

DROP TABLE events

DROP TABLE rate_limit_configs

DROP TABLE api_keys
