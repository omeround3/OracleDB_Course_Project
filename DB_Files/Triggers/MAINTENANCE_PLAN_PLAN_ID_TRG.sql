--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger MAINTENANCE_PLAN_PLAN_ID_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "SYSTEM"."MAINTENANCE_PLAN_PLAN_ID_TRG" BEFORE
    INSERT ON maintenance_plan
    FOR EACH ROW
     WHEN ( new.plan_id IS NULL ) BEGIN
    :new.plan_id := maintenance_plan_plan_id_seq.nextval;
END;

/
ALTER TRIGGER "SYSTEM"."MAINTENANCE_PLAN_PLAN_ID_TRG" ENABLE;
