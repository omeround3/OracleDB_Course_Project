declare
   first_name  VARCHAR2(64 BYTE) := 'Meytal';
   last_name  VARCHAR2(64 BYTE) := 'Mitt';
   result number;
begin
   -- Call the function
   result := ADD_TENANT_FUNC(123151, first_name, last_name, 26, 0549361555, 4 , 2050, to_date('24-May-21', 'DD-MON-RR'));
   dbms_output.put_line(result);
end;
/