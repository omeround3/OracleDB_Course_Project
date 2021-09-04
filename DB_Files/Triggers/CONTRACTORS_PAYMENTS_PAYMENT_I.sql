--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger CONTRACTORS_PAYMENTS_PAYMENT_I
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "SYSTEM"."CONTRACTORS_PAYMENTS_PAYMENT_I" BEFORE
    INSERT ON contractors_payments
    FOR EACH ROW
     WHEN ( new.payment_id IS NULL ) BEGIN
    :new.payment_id := contractors_payments_payment_i.nextval;
END;

/
ALTER TRIGGER "SYSTEM"."CONTRACTORS_PAYMENTS_PAYMENT_I" ENABLE;
