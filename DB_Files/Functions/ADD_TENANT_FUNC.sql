--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function ADD_TENANT_FUNC
--------------------------------------------------------

CREATE OR REPLACE EDITIONABLE FUNCTION "SYSTEM"."ADD_TENANT_FUNC" (
     v_id               tenant.tenant_id%type
   , v_first_name       tenant.first_name%type
   , v_last_name        tenant.last_name%type                  
   , v_age              tenant.age%type
   , v_phone            tenant.phone%type
   , v_apartment_id     apartment_tenants.apartment_id%type
   , v_rate             apartment_tenants.rate%type
   , v_last_vote_date   apartment_tenants.last_vote_date%type
) return number
IS
BEGIN
   IF (IS_APARTMENT_FULL(v_apartment_id) = FALSE) THEN
      INSERT INTO TENANT (TENANT_ID, FIRST_NAME, LAST_NAME, AGE, PHONE) 
         VALUES(v_id ,v_first_name, v_last_name, v_age, v_phone);
      INSERT INTO APARTMENT_TENANTS (APARTMENT_ID, TENANT_ID, RATE, LAST_VOTE_DATE) 
         VALUES (v_apartment_id, v_id, v_rate, v_last_vote_date);
      RETURN v_id;
   ELSE
      RETURN -1;
   END IF;
END ADD_TENANT_FUNC;
/
