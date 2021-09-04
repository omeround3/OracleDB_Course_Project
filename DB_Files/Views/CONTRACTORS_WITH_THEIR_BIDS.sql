--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for View CONTRACTORS_WITH_THEIR_BIDS
--------------------------------------------------------

  CREATE OR REPLACE FORCE NONEDITIONABLE VIEW "SYSTEM"."CONTRACTORS_WITH_THEIR_BIDS" ("CONTRACTOR_ID", "MOST_FREQUENT", "CONTRACTOR_NAME") AS 
  select jobs_bids.contractor_id , COUNT(jobs_bids.contractor_id) AS MOST_FREQUENT , contractors.contractor_name
from jobs_bids
LEFT JOIN contractors ON jobs_bids.contractor_id = contractors.contractor_id
GROUP BY jobs_bids.contractor_id,contractors.contractor_name
ORDER BY MOST_FREQUENT DESC
;


