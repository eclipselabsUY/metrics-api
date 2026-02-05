-- upgrade

CREATE INDEX ix_event_types_id ON event_types (id);

-- rollback

DROP INDEX ix_event_types_id ON event_types;
