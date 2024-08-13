-- Node Tables
CREATE TABLE Owner (
  id               INT64 NOT NULL,
  create_time      TIMESTAMP,
  name             STRING(MAX),
  ssn             STRING(MAX),
) PRIMARY KEY (id);

CREATE TABLE Property (
  id               INT64 NOT NULL,
  create_time      TIMESTAMP,
  street_address   STRING(MAX),
) PRIMARY KEY (id);

-- CREATE TABLE Insurer (
--   id               INT64 NOT NULL,
--   create_time      TIMESTAMP,
--   policy           STRING(MAX),
-- ) PRIMARY KEY (id);
-- 
-- CREATE TABLE County (
--   id               INT64 NOT NULL,
-- ) PRIMARY KEY (id);
-- 
-- CREATE TABLE CreditBureau (
--   id               INT64 NOT NULL,
--   create_time      TIMESTAMP,
--   name             STRING(MAX),
-- ) PRIMARY KEY (id);

-- Edge Tables

CREATE TABLE OwnerOwnsProperty (
  id               INT64 NOT NULL,
  property_id       INT64 NOT NULL,
  create_time      TIMESTAMP,
  FOREIGN KEY (property_id) REFERENCES Property (id)
) PRIMARY KEY (id, property_id);

CREATE OR REPLACE PROPERTY GRAPH PropertyGraph 
  NODE TABLES (Owner, Property)
  EDGE TABLES (
    OwnerOwnsProperty
      SOURCE KEY (id) REFERENCES Owner (id)
      DESTINATION KEY (property_id) REFERENCES Property (id)
      LABEL OWNS
  );
