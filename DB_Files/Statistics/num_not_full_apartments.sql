SELECT ap.apartment_id, t.first_name || ' ' || t.last_name as full_name
FROM apartment_payments ap
INNER JOIN tenant t ON ap.tenant_id = t.tenant_id
WHERE EXTRACT(month FROM ap.month) = 5

SELECT ap.tenant_id, SUM(amount) paid_this_month
FROM apartment_payments ap
WHERE EXTRACT(month FROM ap.month) = 5
GROUP BY ap.tenant_id

