-- upgrade

ALTER TABLE event_types ADD COLUMN service_id INTEGER NOT NULL REFERENCES services(id);

-- rollback

ALTER TABLE event_types DROP COLUMN service_id;
