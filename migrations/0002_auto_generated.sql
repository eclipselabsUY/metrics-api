-- upgrade

ALTER TABLE api_keys ADD COLUMN prefix VARCHAR(32) NOT NULL

-- rollback

ALTER TABLE api_keys DROP COLUMN prefix
