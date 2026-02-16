-- upgrade

CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER NOT NULL PRIMARY KEY,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    prefix VARCHAR(32) NOT NULL,
    service_id INTEGER NOT NULL REFERENCES services(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
)

-- rollback

DROP TABLE api_keys
