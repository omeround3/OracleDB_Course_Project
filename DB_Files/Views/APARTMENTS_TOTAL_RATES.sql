--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for View APARTMENTS_TOTAL_RATES
--------------------------------------------------------

  CREATE OR REPLACE FORCE NONEDITIONABLE VIEW "SYSTEM"."APARTMENTS_TOTAL_RATES" ("APARTMENT_ID", "TOTAL_RATE") AS 
  SELECT apartment_id, SUM(rate) total_rate
FROM apartment_tenants
GROUP BY apartment_id WITH READ ONLY
;
