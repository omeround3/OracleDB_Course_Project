SELECT tenant_id
FROM tenant
MINUS
SELECT count_payments.tenant_id
FROM
    (SELECT tenant_id, COUNT(payment_id) payments_amount
    FROM apartment_payments
    WHERE EXTRACT(month FROM month) = 6
    GROUP BY tenant_id) count_payments