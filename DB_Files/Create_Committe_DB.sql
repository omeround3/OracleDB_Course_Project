-- Generated by Oracle SQL Developer Data Modeler 21.2.0.183.1957
--   at:        2021-07-31 16:44:25 IDT
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE apartment (
    apartment_id   INTEGER,
    tenants_number INTEGER NOT NULL,
    "size"         INTEGER NOT NULL
);

ALTER TABLE apartment ADD CONSTRAINT apartment_pk PRIMARY KEY ( apartment_id );

CREATE TABLE apartment_payments (
    payment_id                     INTEGER NOT NULL,
    aparment_id                    INTEGER NOT NULL,
    month                          DATE NOT NULL,
    payment_date                   DATE,
    apartment_tenants_apartment_id INTEGER,
    apartment_tenants_tenant_id    INTEGER
);

ALTER TABLE apartment_payments ADD CONSTRAINT apartment_payments_pk PRIMARY KEY ( payment_id );

CREATE TABLE apartment_tenants (
    apartment_id           INTEGER NOT NULL,
    tenant_id              INTEGER NOT NULL,
    rate                   INTEGER DEFAULT 500 NOT NULL,
    last_vote_date         DATE,
    apartment_apartment_id INTEGER NOT NULL
);

ALTER TABLE apartment_tenants ADD CONSTRAINT apartment_tenants_pk PRIMARY KEY ( apartment_id,
                                                                                tenant_id );

CREATE TABLE candidates (
    candidate_id     INTEGER NOT NULL,
    elections_date   DATE NOT NULL,
    num_supporters   INTEGER DEFAULT 0,
    status           VARCHAR2(32) DEFAULT 'not elected' NOT NULL,
    tenant_tenant_id INTEGER NOT NULL
);

ALTER TABLE candidates
    ADD CONSTRAINT status_constraint CHECK ( status IN ( 'elected', 'not elected' ) );

CREATE UNIQUE INDEX candidates__idx ON
    candidates (
        tenant_tenant_id
    ASC );

ALTER TABLE candidates ADD CONSTRAINT candidates_pk PRIMARY KEY ( candidate_id );

CREATE TABLE contractors (
    contractor_id   INTEGER NOT NULL,
    contractor_name VARCHAR2(64) NOT NULL,
    address         VARCHAR2(128)
);

ALTER TABLE contractors ADD CONSTRAINT contractors_pk PRIMARY KEY ( contractor_id );

CREATE TABLE contractors_payments (
    payment_id          INTEGER NOT NULL,
    job_id              INTEGER NOT NULL,
    "date"              DATE NOT NULL,
    price               INTEGER NOT NULL,
    payment_description CLOB,
    jobs_job_id         INTEGER NOT NULL
);

ALTER TABLE contractors_payments ADD CONSTRAINT contractors_payments_pk PRIMARY KEY ( payment_id );

CREATE TABLE jobs (
    job_id           INTEGER NOT NULL,
    job_type         VARCHAR2(32) NOT NULL,
    tenant_id        INTEGER NOT NULL,
    contractor_id    INTEGER NOT NULL,
    description      CLOB,
    tenant_tenant_id INTEGER NOT NULL
);

ALTER TABLE jobs
    ADD CHECK ( job_type IN ( 'cleaning', 'gardening', 'paint', 'renovation', 'security' ) );

ALTER TABLE jobs ADD CONSTRAINT jobs_pk PRIMARY KEY ( job_id );

CREATE TABLE jobs_bids (
    jobs_job_id               INTEGER NOT NULL,
    contractors_contractor_id INTEGER NOT NULL,
    price                     INTEGER NOT NULL
);

ALTER TABLE jobs_bids ADD CONSTRAINT jobs_bids_pk PRIMARY KEY ( jobs_job_id,
                                                                contractors_contractor_id );

CREATE TABLE jobs_plans (
    maintenance_plan_plan_id INTEGER NOT NULL,
    maintenance_plan_job_id  INTEGER NOT NULL,
    jobs_job_id              INTEGER NOT NULL
);

ALTER TABLE jobs_plans
    ADD CONSTRAINT jobs_plans_pk PRIMARY KEY ( maintenance_plan_plan_id,
                                               maintenance_plan_job_id,
                                               jobs_job_id );

CREATE TABLE maintenance_plan (
    plan_id     INTEGER NOT NULL,
    job_id      INTEGER NOT NULL,
    status      VARCHAR(20) DEFAULT 'waiting' NOT NULL,
    description CLOB
);

COMMENT ON COLUMN maintenance_plan.status IS
    'approved / declined / waiting. Default is waiting.';
    
ALTER TABLE maintenance_plan
    ADD CHECK ( status IN ( 'approved', 'waiting', 'declined' ) );

ALTER TABLE maintenance_plan ADD CONSTRAINT maintenance_plan_pk PRIMARY KEY ( plan_id,
                                                                              job_id );

CREATE TABLE tenant (
    tenant_id                      INTEGER NOT NULL,
    first_name                     VARCHAR2(64) NOT NULL,
    last_name                      VARCHAR2(64) NOT NULL,
    age                            INTEGER NOT NULL,
    phone                          INTEGER NOT NULL,
    apartment_tenants_apartment_id INTEGER NOT NULL,
    apartment_tenants_tenant_id    INTEGER NOT NULL
);

CREATE UNIQUE INDEX tenant__idx ON
    tenant (
        apartment_tenants_apartment_id
    ASC,
        apartment_tenants_tenant_id
    ASC );

ALTER TABLE tenant ADD CONSTRAINT tenant_pk PRIMARY KEY ( tenant_id );

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE apartment_payments
    ADD CONSTRAINT apartment_payments_apartment_tenants_fk FOREIGN KEY ( apartment_tenants_apartment_id,
                                                                         apartment_tenants_tenant_id )
        REFERENCES apartment_tenants ( apartment_id,
                                       tenant_id );

ALTER TABLE apartment_tenants
    ADD CONSTRAINT apartment_tenants_apartment_fk FOREIGN KEY ( apartment_apartment_id )
        REFERENCES apartment ( apartment_id );

ALTER TABLE candidates
    ADD CONSTRAINT candidates_tenant_fk FOREIGN KEY ( tenant_tenant_id )
        REFERENCES tenant ( tenant_id );

ALTER TABLE contractors_payments
    ADD CONSTRAINT contractors_payments_jobs_fk FOREIGN KEY ( jobs_job_id )
        REFERENCES jobs ( job_id );

ALTER TABLE jobs_bids
    ADD CONSTRAINT jobs_bids_contractors_fk FOREIGN KEY ( contractors_contractor_id )
        REFERENCES contractors ( contractor_id );

ALTER TABLE jobs_bids
    ADD CONSTRAINT jobs_bids_jobs_fk FOREIGN KEY ( jobs_job_id )
        REFERENCES jobs ( job_id );

ALTER TABLE jobs_plans
    ADD CONSTRAINT jobs_plans_jobs_fk FOREIGN KEY ( jobs_job_id )
        REFERENCES jobs ( job_id );

ALTER TABLE jobs_plans
    ADD CONSTRAINT jobs_plans_maintenance_plan_fk FOREIGN KEY ( maintenance_plan_plan_id,
                                                                maintenance_plan_job_id )
        REFERENCES maintenance_plan ( plan_id,
                                      job_id );

ALTER TABLE jobs
    ADD CONSTRAINT jobs_tenant_fk FOREIGN KEY ( tenant_tenant_id )
        REFERENCES tenant ( tenant_id );

ALTER TABLE tenant
    ADD CONSTRAINT tenant_apartment_tenants_fk FOREIGN KEY ( apartment_tenants_apartment_id,
                                                             apartment_tenants_tenant_id )
        REFERENCES apartment_tenants ( apartment_id,
                                       tenant_id );



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                            11
-- CREATE INDEX                             2
-- ALTER TABLE                             23
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   1
-- WARNINGS                                 0
