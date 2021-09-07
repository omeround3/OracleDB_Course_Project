--------------------------------------------------------
--  File created - Tuesday-September-07-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Procedure DELETE_TENANT_PROC
--------------------------------------------------------
set define off;

  CREATE OR REPLACE NONEDITIONABLE PROCEDURE "SYSTEM"."DELETE_TENANT_PROC" (
     v_id               tenant.tenant_id%type
) 
IS
BEGIN
    DELETE FROM tenant
    WHERE tenant_id = v_id;
    COMMIT;
END;

/
