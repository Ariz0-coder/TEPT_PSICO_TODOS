-- schema_tept.sql
-- Esquema simplificado para TEPT / Depresión / Ansiedad

CREATE TABLE users (
  id UUID PRIMARY KEY,
  pseudonym TEXT,
  email_hash TEXT,
  role TEXT CHECK (role IN ('patient','therapist','admin')),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE profiles (
  user_id UUID PRIMARY KEY REFERENCES users(id),
  dob_year_bucket INT,
  gender TEXT,
  timezone TEXT,
  preferences JSONB,
  consent_share_anonymized BOOLEAN DEFAULT FALSE,
  consent_clinician_access BOOLEAN DEFAULT FALSE
);

CREATE TABLE assessments (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  type TEXT, -- 'PCL5','PHQ9','GAD7'
  items JSONB,
  total_score SMALLINT,
  language TEXT,
  completed_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE techniques (
  id SERIAL PRIMARY KEY,
  name TEXT,
  script_text TEXT,
  audio_url TEXT,
  indications JSONB
);

CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  technique_id INT REFERENCES techniques(id),
  pre_score SMALLINT,
  post_score SMALLINT,
  notes TEXT,
  duration_seconds INT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE safety_flags (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID REFERENCES sessions(id),
  user_id UUID REFERENCES users(id),
  flag_type TEXT,
  details JSONB,
  action_taken JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE anonymized_exports (
  id UUID PRIMARY KEY,
  generated_by UUID REFERENCES users(id),
  fields_included JSONB,
  salt_hash TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
