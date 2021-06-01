insert overwrite into {da_hr_dm}.dw_dim_employee
select emp.employee_id,
       emp.first_name,
       emp.last_name,
       emp.department_id,
       emp.department_name,
       emp.source_system,
       emp.dw_create_date,
       emp.dw_last_updated
from {da_hr_int}.stg_employee emp