--------------------------------------------------------
--  File created - Friday-September-03-2021   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Trigger APARTMENT_APARTMENT_ID_TRG
--------------------------------------------------------

  CREATE OR REPLACE NONEDITIONABLE TRIGGER "SYSTEM"."APARTMENT_APARTMENT_ID_TRG" BEFORE
    INSERT ON apartment
    FOR EACH ROW
     WHEN ( new.apartment_id IS NULL ) BEGIN
    :new.apartment_id := apartment_apartment_id_seq.nextval;
END;

/
ALTER TRIGGER "SYSTEM"."APARTMENT_APARTMENT_ID_TRG" ENABLE;
