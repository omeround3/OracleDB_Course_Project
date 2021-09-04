--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger JOBS_JOB_ID_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "SYSTEM"."JOBS_JOB_ID_TRG" BEFORE
    INSERT ON jobs
    FOR EACH ROW
     WHEN ( new.job_id IS NULL ) BEGIN
    :new.job_id := jobs_job_id_seq.nextval;
END;

/
ALTER TRIGGER "SYSTEM"."JOBS_JOB_ID_TRG" ENABLE;
