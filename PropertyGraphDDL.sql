-- Node Tables
CREATE TABLE County (
      id		INT64 NOT NULL,
      name		STRING(MAX),
      tax_rate		NUMERIC,
      postcode		STRING(MAX),
    ) PRIMARY KEY (id);
CREATE TABLE Property (
      id		INT64 NOT NULL,
      address		STRING(MAX),
      bedrooms		INT64 NOT NULL,
      bathrooms		INT64 NOT NULL,
      price		INT64 NOT NULL,
    ) PRIMARY KEY (id);
CREATE TABLE Owner (
      id		INT64 NOT NULL,
      name		STRING(MAX),
      ssn		STRING(MAX),
    ) PRIMARY KEY (id);
CREATE TABLE CreditReport (
      id		INT64 NOT NULL,
      score		INT64 NOT NULL,
      bureau		STRING(MAX),
    ) PRIMARY KEY (id);
-- Edge Tables

CREATE TABLE HasCreditReport (
      id		INT64 NOT NULL,
      report_id		INT64 NOT NULL,
      create_date		STRING(MAX),
    FOREIGN KEY (report_id) REFERENCES Owner (id)
) PRIMARY KEY (id, report_id),
  INTERLEAVE IN PARENT Owner ON DELETE CASCADE;

CREATE TABLE InCounty (
      id		INT64 NOT NULL,
      county_id		INT64 NOT NULL,
      property_id		INT64 NOT NULL,
      create_date		STRING(MAX),
    FOREIGN KEY (property_id) REFERENCES Property (id)
) PRIMARY KEY (id, property_id),
  INTERLEAVE IN PARENT Property ON DELETE CASCADE;

CREATE TABLE HasOwner (
      id		INT64 NOT NULL,
      property_id		INT64 NOT NULL,
      owner_id		INT64 NOT NULL,
      create_date		STRING(MAX),
    FOREIGN KEY (owner_id) REFERENCES Property (id)
) PRIMARY KEY (id, owner_id),
  INTERLEAVE IN PARENT Property ON DELETE CASCADE;
-- Graph Declaration
CREATE OR REPLACE PROPERTY GRAPH ProperyGraph
  NODE TABLES (
    County,
    Property,
    Owner,
    CreditReport
  )
  EDGE TABLES (
    
HasOwner
      SOURCE KEY (id) REFERENCES Property (id)
      DESTINATION KEY (owner_id) REFERENCES Property (id)
      LABEL HasOwner,
    
InCounty
      SOURCE KEY (id) REFERENCES Property (id)
      DESTINATION KEY (property_id) REFERENCES Property (id)
      LABEL InCounty,
    
HasCreditReport
      SOURCE KEY (id) REFERENCES Owner (id)
      DESTINATION KEY (report_id) REFERENCES Owner (id)
      LABEL HasCreditReport
);
