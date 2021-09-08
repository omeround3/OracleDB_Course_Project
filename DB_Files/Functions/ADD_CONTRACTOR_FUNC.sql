--------------------------------------------------------
--  File created - Wednesday-September-08-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function ADD_CONTRACTOR_FUNC
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."ADD_CONTRACTOR_FUNC" (
     v_contractor_id              contractors.contractor_id%type  
   , v_contractor_name            contractors.contractor_name%type               
   , v_address                    contractors.address%type
) return number
IS
BEGIN
      INSERT INTO CONTRACTORS (contractor_id, contractor_name, address) 
         VALUES(v_contractor_id, v_contractor_name, v_address);
     RETURN v_contractor_id;
END ADD_CONTRACTOR_FUNC;

/
