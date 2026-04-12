-- upgrade

CREATE TABLE IF NOT EXISTS events (
    id UUID NOT NULL PRIMARY KEY,
    service_id INTEGER,
    event_type VARCHAR(255) NOT NULL,
    method VARCHAR(16),
    url VARCHAR(2048),
    client_ip VARCHAR(45),
    event_metadata VARCHAR(65535),
    timestamp VARCHAR(32)
)

CREATE TABLE IF NOT EXISTS page_views (
    id UUID NOT NULL PRIMARY KEY,
    service_id INTEGER,
    path VARCHAR(2048) NOT NULL,
    referrer VARCHAR(2048),
    user_agent VARCHAR(512),
    viewport VARCHAR(20),
    document_title VARCHAR(512),
    client_ip VARCHAR(45),
    timestamp VARCHAR(32)
)

-- rollback

DROP TABLE page_views

DROP TABLE events
