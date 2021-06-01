insert overwrite into {da_hr_int}.stg_employee
select emp.id employee_id,
       emp.first_name,
       emp.last_name,
       emp.department_id,
       dep.department_name,
       emp.source_system,
       CURRENT_TIMESTAMP AS dw_create_date,
       emp.last_updated AS dw_last_updated
from {dwh_prod}.employee emp left join {dwh_prod}.department dep
on emp.department_id = dep.id