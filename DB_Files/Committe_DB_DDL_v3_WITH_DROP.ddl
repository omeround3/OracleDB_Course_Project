--   The following DDL script will create the committe tables



DROP TABLE apartment CASCADE CONSTRAINTS;

DROP TABLE apartment_payments CASCADE CONSTRAINTS;

DROP TABLE apartment_tenants CASCADE CONSTRAINTS;

DROP TABLE candidates CASCADE CONSTRAINTS;

DROP TABLE contractors CASCADE CONSTRAINTS;

DROP TABLE contractors_payments CASCADE CONSTRAINTS;

DROP TABLE jobs CASCADE CONSTRAINTS;

DROP TABLE jobs_bids CASCADE CONSTRAINTS;

DROP TABLE jobs_plans CASCADE CONSTRAINTS;

DROP TABLE maintenance_plan CASCADE CONSTRAINTS;

DROP TABLE tenant CASCADE CONSTRAINTS;

drop sequence "SYSTEM"."APARTMENT_APARTMENT_ID_SEQ";

drop sequence "SYSTEM"."APARTMENT_PAYMENTS_PAYMENT_ID";

drop sequence "SYSTEM"."CONTRACTORS_PAYMENTS_PAYMENT_I";

drop sequence "SYSTEM"."JOBS_JOB_ID_SEQ";

drop sequence "SYSTEM"."MAINTENANCE_PLAN_PLAN_ID_SEQ";


-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE apartment (
    apartment_id   INTEGER NOT NULL,
    tenants_number INTEGER DEFAULT 1 NOT NULL CHECK ( tenants_number BETWEEN 1 AND 8 ),
    "size"         INTEGER DEFAULT 50 NOT NULL
);

ALTER TABLE apartment ADD CONSTRAINT apartment_pk PRIMARY KEY ( apartment_id );

CREATE TABLE apartment_payments (
    payment_id   INTEGER NOT NULL,
    tenant_id    INTEGER NOT NULL,
    apartment_id INTEGER NOT NULL,
    month        DATE NOT NULL,
    payment_date DATE NOT NULL,
    amount       INTEGER CHECK ( amount >= 0 )
);

ALTER TABLE apartment_payments ADD CONSTRAINT apartment_payments_pk PRIMARY KEY ( payment_id );

CREATE TABLE apartment_tenants (
    apartment_id   INTEGER NOT NULL,
    tenant_id      INTEGER NOT NULL,
    rate           INTEGER DEFAULT 500 NOT NULL CHECK ( rate >= 0 ),
    last_vote_date DATE
);

CREATE UNIQUE INDEX apartment_tenants__idx ON
    apartment_tenants (
        tenant_id
    ASC );

ALTER TABLE apartment_tenants ADD CONSTRAINT apartment_tenants_pk PRIMARY KEY ( apartment_id,
                                                                                tenant_id );

CREATE TABLE candidates (
    candidate_id   INTEGER NOT NULL,
    elections_date DATE NOT NULL,
    num_supporters INTEGER DEFAULT 0 NOT NULL,
    status         VARCHAR2(32) DEFAULT 'not elected' NOT NULL
        CONSTRAINT status_constraint CHECK ( status IN ( 'elected', 'not elected' ) )
);

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
    payment_date        DATE NOT NULL,
    price               INTEGER NOT NULL CHECK ( price >= 0 ),
    payment_description CLOB
);

ALTER TABLE contractors_payments ADD CONSTRAINT contractors_payments_pk PRIMARY KEY ( payment_id );

CREATE TABLE jobs (
    job_id      INTEGER NOT NULL,
    job_type    VARCHAR2(32) NOT NULL CHECK ( job_type IN ( 'cleaning', 'horticulture', 'plumbing', 'renovation', 'security' ) ),
    tenant_id   INTEGER NOT NULL,
    description CLOB
);

ALTER TABLE jobs ADD CONSTRAINT jobs_pk PRIMARY KEY ( job_id );

CREATE TABLE jobs_bids (
    contractor_id INTEGER NOT NULL,
    job_id        INTEGER NOT NULL,
    price         INTEGER CHECK ( price >= 0 )
);

ALTER TABLE jobs_bids ADD CONSTRAINT jobs_bids_pk PRIMARY KEY ( contractor_id,
                                                                job_id );

CREATE TABLE jobs_plans (
    plan_id INTEGER NOT NULL,
    job_id  INTEGER NOT NULL
);

ALTER TABLE jobs_plans ADD CONSTRAINT jobs_plans_pk PRIMARY KEY ( plan_id,
                                                                  job_id );

CREATE TABLE maintenance_plan (
    plan_id     INTEGER NOT NULL,
    status      VARCHAR2(20) DEFAULT 'waiting' NOT NULL CHECK ( status IN ( 'approved', 'declined', 'waiting' ) ),
    description CLOB
);

COMMENT ON COLUMN maintenance_plan.status IS
    'The default value is ''waiting''';

ALTER TABLE maintenance_plan ADD CONSTRAINT maintenance_plan_pk PRIMARY KEY ( plan_id );

CREATE TABLE tenant (
    tenant_id  INTEGER NOT NULL,
    first_name VARCHAR2(64) NOT NULL,
    last_name  VARCHAR2(64) NOT NULL,
    age        INTEGER NOT NULL CHECK ( age >= 0 ),
    phone      INTEGER NOT NULL
);

ALTER TABLE tenant ADD CONSTRAINT tenant_pk PRIMARY KEY ( tenant_id );

ALTER TABLE apartment_payments
    ADD CONSTRAINT ap__a_fk FOREIGN KEY ( apartment_id )
        REFERENCES apartment ( apartment_id )
        ON DELETE CASCADE;
        
ALTER TABLE apartment_payments
    ADD CONSTRAINT apartment_payments_tenant_fk FOREIGN KEY ( tenant_id )
        REFERENCES tenant ( tenant_id )
        ON DELETE CASCADE;

ALTER TABLE apartment_tenants
    ADD CONSTRAINT at_a_fk FOREIGN KEY ( apartment_id )
        REFERENCES apartment ( apartment_id )
        ON DELETE CASCADE;

ALTER TABLE apartment_tenants
    ADD CONSTRAINT at_t_fk FOREIGN KEY ( tenant_id )
        REFERENCES tenant ( tenant_id )
        ON DELETE CASCADE;

ALTER TABLE contractors_payments
    ADD CONSTRAINT cp_jobs_fk FOREIGN KEY ( job_id )
        REFERENCES jobs ( job_id )
        ON DELETE CASCADE;

ALTER TABLE candidates
    ADD CONSTRAINT ct_fk FOREIGN KEY ( candidate_id )
        REFERENCES tenant ( tenant_id )
        ON DELETE CASCADE;

ALTER TABLE jobs_bids
    ADD CONSTRAINT jb_c_fk FOREIGN KEY ( contractor_id )
        REFERENCES contractors ( contractor_id )
        ON DELETE CASCADE;

ALTER TABLE jobs_bids
    ADD CONSTRAINT jb_j_fk FOREIGN KEY ( job_id )
        REFERENCES jobs ( job_id )
        ON DELETE CASCADE;

ALTER TABLE jobs
    ADD CONSTRAINT jobs_tenant_fk FOREIGN KEY ( tenant_id )
        REFERENCES tenant ( tenant_id )
        ON DELETE CASCADE;

ALTER TABLE jobs_plans
    ADD CONSTRAINT jp_j_fk FOREIGN KEY ( job_id )
        REFERENCES jobs ( job_id )
        ON DELETE CASCADE;

ALTER TABLE jobs_plans
    ADD CONSTRAINT jp_mp_fk FOREIGN KEY ( plan_id )
        REFERENCES maintenance_plan ( plan_id )
        ON DELETE CASCADE;

CREATE SEQUENCE apartment_apartment_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER apartment_apartment_id_trg BEFORE
    INSERT ON apartment
    FOR EACH ROW
    WHEN ( new.apartment_id IS NULL )
BEGIN
    :new.apartment_id := apartment_apartment_id_seq.nextval;
END;
/

CREATE SEQUENCE apartment_payments_payment_id START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER apartment_payments_payment_id BEFORE
    INSERT ON apartment_payments
    FOR EACH ROW
    WHEN ( new.payment_id IS NULL )
BEGIN
    :new.payment_id := apartment_payments_payment_id.nextval;
END;
/

CREATE SEQUENCE contractors_payments_payment_i START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER contractors_payments_payment_i BEFORE
    INSERT ON contractors_payments
    FOR EACH ROW
    WHEN ( new.payment_id IS NULL )
BEGIN
    :new.payment_id := contractors_payments_payment_i.nextval;
END;
/

CREATE SEQUENCE jobs_job_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER jobs_job_id_trg BEFORE
    INSERT ON jobs
    FOR EACH ROW
    WHEN ( new.job_id IS NULL )
BEGIN
    :new.job_id := jobs_job_id_seq.nextval;
END;
/

CREATE SEQUENCE maintenance_plan_plan_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER maintenance_plan_plan_id_trg BEFORE
    INSERT ON maintenance_plan
    FOR EACH ROW
    WHEN ( new.plan_id IS NULL )
BEGIN
    :new.plan_id := maintenance_plan_plan_id_seq.nextval;
END;
/