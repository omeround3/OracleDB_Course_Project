--------------------------------------------------------
--  File created - Wednesday-September-08-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Function ADD_JOB_PAYMENT
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE FUNCTION "SYSTEM"."ADD_JOB_PAYMENT" (
     v_job_id                contractors_payments.job_id%type               
   , v_payment_date                 contractors_payments.payment_date%type
   , v_price                 contractors_payments.price%type
   , v_payment_description   contractors_payments.payment_description%type
) return number
IS
BEGIN
      INSERT INTO CONTRACTORS_PAYMENTS (payment_id, job_id, payment_date, price, payment_description) 
         VALUES(CONTRACTORS_PAYMENTS_PAYMENT_I.nextval, v_job_id, v_payment_date, v_price, v_payment_description);
     RETURN CONTRACTORS_PAYMENTS_PAYMENT_I.currval;
END ADD_JOB_PAYMENT;

/
