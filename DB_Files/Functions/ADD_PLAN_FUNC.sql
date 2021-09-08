--------------------------------------------------------
--  File created - Thursday-September-09-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function ADD_PLAN_FUNC
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."ADD_PLAN_FUNC" (
     v_job_id             jobs.job_id%type               
   , v_description          jobs.description %type
) return number
IS
    v_plan_id NUMBER;
BEGIN
    v_plan_id := MAINTENANCE_PLAN_PLAN_ID_SEQ.nextval;
    INSERT INTO MAINTENANCE_PLAN (plan_id, description) 
         VALUES(v_plan_id, v_description);
    INSERT INTO JOBS_PLANS (plan_id, job_id) VALUES(v_plan_id, v_job_id);
    RETURN MAINTENANCE_PLAN_PLAN_ID_SEQ.currval;
END ADD_PLAN_FUNC;

/
