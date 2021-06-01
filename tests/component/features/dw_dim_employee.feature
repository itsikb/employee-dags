Feature: Trigger dw_dim_employee DAG for Snowflake

  Scenario: dw_dim_employee DAG run successfully for Snowflake

    Given [SF] I create schema dwh_prod

    And [SF] I create schema da_hr_int

    And [SF] I create schema da_hr_dm

    And [SF] I create under schema dwh_prod the following tables
      | tables     |
      | employee   |
      | department |

    And [SF] I create under schema da_hr_int the following tables
      | tables       |
      | stg_employee |

    And [SF] I create under schema da_hr_dm the following tables
      | tables          |
      | dw_dim_employee |

    And [SF] I insert into table dwh_prod.department the following records
      | id | department_name | last_updated          | source_system |
      | 1  | 'Sales'         | '2021-06-01 00:01:00' | 'HILAN'       |
      | 2  | 'Finance'       | '2021-06-02 00:01:30' | 'HILAN'       |
      | 3  | 'Marketing'     | '2021-06-02 00:02:15' | 'HILAN'       |

    And [SF] I insert into table dwh_prod.employee the following records
      | id | first_name | last_name  | department_id | last_updated          | source_system |
      | 1  | 'Lisa'     | 'Simpson'  |             2 | '2021-06-03 00:01:00' | 'HILAN'       |
      | 2  | 'Sheldon'  | 'Cooper'   |             1 | '2021-06-06 00:01:30' | 'HILAN'       |
      | 3  | 'Fred'     | 'Flinston' |             1 | '2021-06-07 00:02:15' | 'HILAN'       |

    And I unpause DAG dw_dim_employee

    When [SF] I trigger SF dynamic DAG dw_dim_employee with the following key-values

    Then I expect DAG dw_dim_employee to have finished successfully

    And [SF] I expect the results in table da_hr_dm.dw_dim_employee to be equal to
      | employee_id | first_name | last_name | department_id | department_name | source_system |
      | 1           | Lisa       | Simpson   | 2             | Finance         | HILAN         |
      | 2           | Sheldon    | Cooper    | 1             | Sales           | HILAN         |
      | 3           | Fred       | Flinston  | 1             | Sales           | HILAN         |
