CREATE OR REPLACE FUNCTION IS_APARTMENT_FULL (
    v_apartment_id     apartment.apartment_id%type
) RETURN BOOLEAN
IS
    max_tenants_number NUMBER;
    current_tenant_number NUMBER;
BEGIN
    -- Get maximum tenants number in a given apartment
    SELECT
    a.tenants_number INTO max_tenants_number
    FROM apartment a
    WHERE a.apartment_id = v_apartment_id;
    -- Get current tenant number in a given apartment
    SELECT 
    COUNT(ap.apartment_id) INTO current_tenant_number
    FROM apartment_tenants ap
    WHERE ap.apartment_id = v_apartment_id
    GROUP BY ap.apartment_id;
    -- Check if current tenant number is greater than the maximum tenant number in the apartment
    IF (current_tenant_number >= max_tenants_number) THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END;