SELECT COUNT(apartment_id) 
FROM apartment_occupancy ao
WHERE DECODE(ao.max_number_tenants - ao.current_number_tenants, 0 , 'FULL', 'NOT FULL') = 'NOT FULL'