SELECT 
        (t.first_name ||'  '|| t.last_name) full_name, 
        t.age, 
        c.num_supporters
FROM tenant t 
LEFT JOIN candidates c ON t.tenant_id = c.candidate_id 
WHERE c.status = 'elected'
ORDER BY 
    c.num_supporters DESC 
