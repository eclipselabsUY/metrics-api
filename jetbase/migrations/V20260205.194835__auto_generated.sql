-- upgrade

CREATE TABLE api_keys (
    id INTEGER NOT NULL PRIMARY KEY,
    key_hash VARCHAR(255) NOT NULL,
    service_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services (id)
);

CREATE TABLE service_types (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    kind VARCHAR(8) NOT NULL
);

CREATE TABLE services (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50),
    url VARCHAR(150),
    service_type_id INTEGER NOT NULL,
    FOREIGN KEY (service_type_id) REFERENCES service_types (id)
);

-- rollback

DROP TABLE api_keys;

DROP TABLE service_types;

DROP TABLE services;
