--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger APARTMENT_PAYMENTS_PAYMENT_ID
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "SYSTEM"."APARTMENT_PAYMENTS_PAYMENT_ID" BEFORE
    INSERT ON apartment_payments
    FOR EACH ROW
     WHEN ( new.payment_id IS NULL ) BEGIN
    :new.payment_id := apartment_payments_payment_id.nextval;
END;

/
ALTER TRIGGER "SYSTEM"."APARTMENT_PAYMENTS_PAYMENT_ID" ENABLE;
