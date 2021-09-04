DECLARE
  V_APARTMENT_ID NUMBER;
  v_Return BOOLEAN;
BEGIN
  V_APARTMENT_ID := 4;

  v_Return := IS_APARTMENT_FULL(
    V_APARTMENT_ID => V_APARTMENT_ID
  );

IF (v_Return) THEN 
    DBMS_OUTPUT.PUT_LINE('v_Return = ' || 'TRUE');
  ELSE
    DBMS_OUTPUT.PUT_LINE('v_Return = ' || 'FALSE');
  END IF;
  --:v_Return := v_Return;
--rollback; 
END;
