SELECT 
    at.apartment_id, 
    at.tenant_id,
    t.first_name || ' ' || t.last_name as full_name,
    at.rate
FROM
    (SELECT debts.tenant_id
    FROM
        (SELECT DISTINCT
            ap.apartment_id, 
            ap.tenant_id,
            mp.monthly_sum,
            (SELECT at.rate FROM apartment_tenants at WHERE at.tenant_id = ap.tenant_id) as rate
        FROM 
            apartment_payments ap,
            (SELECT tenant_id, SUM(amount) monthly_sum
            FROM apartment_payments 
            WHERE EXTRACT(month FROM month) BETWEEN 4 AND 5
            GROUP BY tenant_id) mp
        WHERE ap.tenant_id = mp.tenant_id) debts
    WHERE debts.monthly_sum < debts.rate
    UNION
    (SELECT tenant_id
    FROM tenant
    MINUS
    SELECT count_payments.tenant_id
    FROM
        (SELECT tenant_id, COUNT(payment_id) payments_amount
        FROM apartment_payments
        WHERE EXTRACT(month FROM month) BETWEEN 4 AND 5
        GROUP BY tenant_id) count_payments)
    ) tenants_debts,
    apartment_tenants at,
    tenant t
WHERE tenants_debts.tenant_id = at.tenant_id
AND at.tenant_id = t.tenant_id