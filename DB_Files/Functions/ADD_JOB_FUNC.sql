--------------------------------------------------------
--  File created - Wednesday-September-08-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function ADD_JOB_FUNC
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."ADD_JOB_FUNC" (
     v_job_type             jobs.job_type%type               
   , v_tenant_id            jobs.tenant_id%type
   , v_description          jobs.description %type
) return number
IS
BEGIN
      INSERT INTO JOBS (job_id, job_type, tenant_id, description) 
         VALUES(JOBS_JOB_ID_SEQ.nextval, v_job_type, v_tenant_id, v_description);
     RETURN JOBS_JOB_ID_SEQ.currval;
END ADD_JOB_FUNC;

/
