--------------------------------------------------------
--  File created - Tuesday-September-07-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function UPDATE_TENANT_FUNC
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE FUNCTION "SYSTEM"."UPDATE_TENANT_FUNC" (
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
   Cursor c_tenant
   IS
   SELECT COUNT(1) 
   FROM tenant
   WHERE tenant_id = v_id;

   n_count NUMBER;
BEGIN
   -- Check if the tenant exists
   OPEN c_tenant;
   FETCH c_tenant INTO n_count;
   close c_tenant;
   -- Update the tenant if exists
   IF n_count > 0 THEN
      -- Update tenant details by tenant id
      UPDATE TENANT
      SET  
         FIRST_NAME = v_first_name, 
         LAST_NAME = v_last_name, 
         AGE = v_age, 
         PHONE = v_phone
      WHERE tenant_id = v_id;
      -- Update apartment_tenants details by tenant id
      UPDATE APARTMENT_TENANTS 
      SET
         APARTMENT_ID = v_apartment_id, 
         RATE = v_rate, 
         LAST_VOTE_DATE = v_last_vote_date
      WHERE tenant_id = v_id;
      COMMIT;
      RETURN v_id;
   -- Return -1 if the tenant doesn't exists
   ELSE
      RETURN -1;
   END IF;
END UPDATE_TENANT_FUNC;

/
