CREATE TABLE Owner (
  id               INT64 NOT NULL,
  create_time      TIMESTAMP,
  name             STRING(MAX),
) PRIMARY KEY (id);

CREATE TABLE Property (
  id               INT64 NOT NULL,
  create_time      TIMESTAMP,
) PRIMARY KEY (id);

CREATE TABLE Insurer (
  id               INT64 NOT NULL,
  account_id       INT64 NOT NULL,
  create_time      TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES Owner (id)
) PRIMARY KEY (id, account_id),
  INTERLEAVE IN PARENT Property ON DELETE CASCADE;

#CREATE TABLE AccountTransferAccount (
#  id               INT64 NOT NULL,
#  to_id            INT64 NOT NULL,
#  amount           FLOAT64,
#  create_time      TIMESTAMP NOT NULL,
#  order_number     STRING(MAX),
#  FOREIGN KEY (to_id) REFERENCES Account (id)
#) PRIMARY KEY (id, to_id, create_time),
#  INTERLEAVE IN PARENT Account ON DELETE CASCADE;

CREATE OR REPLACE PROPERTY GRAPH FinGraph
  NODE TABLES (Owner, Propery, Insurer)
  EDGE TABLES (
    PersonOwnProperty
      SOURCE KEY (id) REFERENCES Owner (id)
      DESTINATION KEY (account_id) REFERENCES Property (id)
      LABEL Owns,
    InsuresProperty
      SOURCE KEY (id) REFERENCES Insurer (id)
      DESTINATION KEY (to_id) REFERENCES Property (id)
      LABEL Transfers
  );
