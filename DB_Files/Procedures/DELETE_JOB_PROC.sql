--------------------------------------------------------
--  File created - Wednesday-September-08-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Procedure DELETE_JOB_PROC
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."DELETE_JOB_PROC" (
     v_id               jobs.job_id%type
) 
IS
BEGIN
    DELETE FROM jobs
    WHERE job_id = v_id;
    COMMIT;
END;

/
