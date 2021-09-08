--------------------------------------------------------
--  File created - Wednesday-September-08-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for View APARTMENT_OCCUPANCY
--------------------------------------------------------

  CREATE OR REPLACE FORCE NONEDITIONABLE VIEW "SYSTEM"."APARTMENT_OCCUPANCY" ("APARTMENT_ID", "CURRENT_NUMBER_TENANTS", "MAX_NUMBER_TENANTS") AS 
  SELECT 
    ap.apartment_id, 
    COUNT(ap.apartment_id) as Current_Number_Tenants,
    (SELECT tenants_number FROM apartment WHERE apartment.apartment_id = ap.apartment_id) as Max_Number_Tenants
FROM apartment_tenants ap
GROUP BY ap.apartment_id WITH READ ONLY;

   COMMENT ON TABLE "SYSTEM"."APARTMENT_OCCUPANCY"  IS 'This view will show how many tenants there are in each apartment and if there is a place to add more tenants to this apartment.'
;
