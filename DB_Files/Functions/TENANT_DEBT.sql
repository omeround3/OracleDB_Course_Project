--------------------------------------------------------
--  File created - Thursday-September-09-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function TENANT_DEBT
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."TENANT_DEBT" (
    v_tenant_id     tenant.tenant_id%type,
    v_month         NUMBER
) RETURN NUMBER
IS
    tenant_rate NUMBER;
    paid NUMBER := 0;
    debt NUMBER := 0;

    -- cursor to get number of tenant payments
    Cursor c_ap
    IS
    SELECT COUNT(1) 
    FROM apartment_payments ap
    WHERE ap.tenant_id = v_tenant_id;

    n_count NUMBER;
BEGIN
    -- Get tenant rate
    SELECT rate INTO tenant_rate
    FROM apartment_tenants at
    WHERE at.tenant_id = v_tenant_id;
    -- Get payments of tenants; if exists
    OPEN c_ap;
    FETCH c_ap INTO n_count;
    close c_ap;
    IF n_count > 0 THEN
        -- Sum amount of payments for a given tenant id
        SELECT SUM(amount) INTO paid
        FROM apartment_payments 
        WHERE EXTRACT(month FROM apartment_payments.month) = v_month
        AND tenant_id = v_tenant_id
        GROUP BY tenant_id;
        debt := tenant_rate - paid;
        RETURN debt;
    ELSE
        RETURN tenant_rate;
    END IF;
END;

/
