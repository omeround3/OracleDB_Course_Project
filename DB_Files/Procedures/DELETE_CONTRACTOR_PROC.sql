--------------------------------------------------------
--  File created - Wednesday-September-08-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Procedure DELETE_CONTRACTOR_PROC
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."DELETE_CONTRACTOR_PROC" (
     v_id               contractors.contractor_id%type
) 
IS
BEGIN
    DELETE FROM contractors
    WHERE contractor_id = v_id;
    COMMIT;
END;

/
