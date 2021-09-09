SELECT *
FROM
    (SELECT 
        ap.apartment_id, 
        ap.tenant_id,
        mp.monthly_sum,
        (SELECT at.rate FROM apartment_tenants at WHERE at.tenant_id = ap.tenant_id) as rate
    FROM 
        apartment_payments ap,
        (SELECT tenant_id, SUM(amount) monthly_sum
        FROM apartment_payments 
        WHERE EXTRACT(month FROM month) = 5
        GROUP BY tenant_id) mp
    WHERE ap.tenant_id = mp.tenant_id) debts
WHERE debts.monthly_sum < debts.rate








