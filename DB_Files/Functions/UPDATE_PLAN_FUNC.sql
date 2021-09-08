--------------------------------------------------------
--  File created - Thursday-September-09-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function UPDATE_PLAN_FUNC
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."UPDATE_PLAN_FUNC" (
     v_plan_id          maintenance_plan.plan_id%type
   , v_status           maintenance_plan.status%type
) return number
IS
   Cursor c_mp
   IS
   SELECT COUNT(1) 
   FROM maintenance_plan
   WHERE plan_id = v_plan_id;

   n_count NUMBER;
BEGIN
   -- Check if the plan exists
   OPEN c_mp;
   FETCH c_mp INTO n_count;
   close c_mp;
   -- Update the plan if exists
   IF n_count > 0 THEN
      -- Update plan status by plan id
      UPDATE maintenance_plan
      SET status = v_status 
      WHERE plan_id = v_plan_id;

      COMMIT;
      RETURN v_plan_id;
   -- Return -1 if the plan doesn't exists
   ELSE
      RETURN -1;
   END IF;
END UPDATE_PLAN_FUNC;

/
