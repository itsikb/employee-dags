CREATE TABLE {da_hr_int}.stg_employee
(
    employee_id     bigint NOT NULL PRIMARY KEY,
    first_name      varchar(50) NOT NULL,
    last_name       varchar(50) NOT NULL,
    department_id   bigint NOT NULL,
    department_name varchar(50) NOT NULL,
    source_system   varchar(50) NOT NULL,
    dw_create_date  timestamp NOT NULL,
    dw_last_updated timestamp NOT NULL
)
