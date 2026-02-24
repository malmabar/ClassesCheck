-- Morning Classes Check - PostgreSQL isolation bootstrap
-- Run as a PostgreSQL superuser (for example: postgres).
-- This creates a dedicated role, database, and schemas for this project.

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mc_app') THEN
    CREATE ROLE mc_app LOGIN PASSWORD 'change_me_with_a_strong_password' NOSUPERUSER NOCREATEDB NOCREATEROLE;
  END IF;
END
$$;

-- CREATE DATABASE cannot run inside DO/transaction block.
SELECT 'CREATE DATABASE morning_classes_check OWNER mc_app'
WHERE NOT EXISTS (
  SELECT 1 FROM pg_database WHERE datname = 'morning_classes_check'
)\gexec

\connect morning_classes_check

CREATE SCHEMA IF NOT EXISTS mc_core AUTHORIZATION mc_app;
CREATE SCHEMA IF NOT EXISTS mc_meta AUTHORIZATION mc_app;

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON DATABASE morning_classes_check FROM PUBLIC;

GRANT CONNECT ON DATABASE morning_classes_check TO mc_app;
GRANT USAGE, CREATE ON SCHEMA mc_core TO mc_app;
GRANT USAGE, CREATE ON SCHEMA mc_meta TO mc_app;

ALTER ROLE mc_app IN DATABASE morning_classes_check SET search_path = mc_core, public;
