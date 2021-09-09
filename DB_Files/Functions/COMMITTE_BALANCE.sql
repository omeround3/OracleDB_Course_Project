--------------------------------------------------------
--  File created - Thursday-September-09-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function COMMITTE_BALANCE
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."COMMITTE_BALANCE" RETURN NUMBER
IS
    total_tenants_payments NUMBER;
    total_contractors_payments NUMBER;
    v_result NUMBER;
BEGIN
    -- Sum up tenants payments
    SELECT SUM(ap.amount * 0.3) INTO total_tenants_payments
    FROM apartment_payments ap;
    -- Sum up contractors payments
    SELECT SUM(cp.price) INTO total_contractors_payments
    FROM contractors_payments cp;
    -- Substract and return amount
    v_result := total_tenants_payments - total_contractors_payments;
    RETURN v_result;
END;

/
