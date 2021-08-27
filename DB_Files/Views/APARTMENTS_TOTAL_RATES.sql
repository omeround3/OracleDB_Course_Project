CREATE VIEW APARTMENTS_TOTAL_RATES
AS SELECT apartment_id, SUM(rate) total_rate
FROM apartment_tenants
GROUP BY apartment_id WITH READ ONLY;
