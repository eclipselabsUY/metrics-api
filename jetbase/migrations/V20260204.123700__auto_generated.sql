-- upgrade

CREATE INDEX ix_events_id ON events (id);

-- rollback

DROP INDEX ix_events_id ON events;
