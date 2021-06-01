CREATE TABLE {dwh_prod}.department
(
    id              bigint,
    department_name varchar(50),
    source_system   varchar(50),
    last_updated    timestamp
)