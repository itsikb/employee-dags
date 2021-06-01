CREATE TABLE {da_hr_dm}.dw_dim_employee
(
    employee_id     bigint NOT NULL PRIMARY KEY comment 'Employee id',
    first_name      varchar(50) NOT NULL comment 'Employee first name as it appears on her badge.',
    last_name       varchar(50) NOT NULL comment 'Employee last name as it appears on her badge.',
    department_id   bigint NOT NULL comment 'Department id. Reference to dw_dim_department.',
    department_name varchar(50) NOT NULL comment 'Department name',
    source_system   varchar(50) NOT NULL comment 'Source system',
    dw_create_date  timestamp NOT NULL,
    dw_last_updated timestamp NOT NULL
)