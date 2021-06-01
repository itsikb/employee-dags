CREATE TABLE {dwh_prod}.employee
(
    id            bigint,
    first_name    varchar(50),
    last_name     varchar(50),
    department_id bigint,
    source_system varchar(50),
    last_updated  timestamp
)