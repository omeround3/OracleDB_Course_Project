CREATE OR REPLACE VIEW APARTMENT_OCCUPANCY
AS SELECT 
    ap.apartment_id, 
    COUNT(ap.apartment_id) as "Current Number of Tenants",
    (SELECT tenants_number FROM apartment WHERE apartment.apartment_id = ap.apartment_id) as "Max Number of Tenants"
FROM apartment_tenants ap
GROUP BY ap.apartment_id
WITH READ ONLY;

COMMENT ON TABLE APARTMENT_OCCUPANCY IS 'This view will show how many tenants there are in each apartment and if there is a place to add more tenants to this apartment.';
