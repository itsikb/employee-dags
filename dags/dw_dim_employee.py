from datetime import datetime, timedelta
from airflow import DAG

from airflowbigdataoperators.com.kenshoo.helpers.datagate.namespaces import DatagateEngineType
from airflowbigdataoperators.com.kenshoo.helpers.datagate.snowflake_schema_resolver import SnowflakeSchemaResolver
from airflowbigdataoperators.com.kenshoo.operators.datagate_query_operator import DataGateQueryOperator

from employee_dags.conf import AppConfiguration

START_DATE = datetime(2021, 1, 1)
PROCESS_NAME = DAG_ID = 'dw_dim_employee'
SCHEMAS = SnowflakeSchemaResolver.resolve(AppConfiguration, ['dwh_prod', 'da_employee_int', 'da_employee_dm'])

dag_args = {
    'owner': AppConfiguration.default.owner,
    'start_date': START_DATE,
    'datagate_host': AppConfiguration.datagate.url,
    'datagate_token': AppConfiguration.datagate.token,
    'email': AppConfiguration.default.alert.email,
    'datagate_engine': DatagateEngineType.sf,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'query_folder': 'employee_dags/include/sql_files/dw_dim_employee',
    'retry_delay': timedelta(seconds=1)
}

dag = DAG(
    dag_id=DAG_ID,
    default_args=dag_args,
    schedule_interval=AppConfiguration.applications.dw_dim_employee.schedule_interval
)

stg_employee_task = DataGateQueryOperator(
    task_id='stg_employee',
    query_file='1_stg_employee.sql',
    dag=dag
)

dw_dim_employee_task = DataGateQueryOperator(
    task_id='dw_dim_employee',
    query_file='2_dw_dim_employee.sql',
    dag=dag
)

stg_employee_task >> dw_dim_employee_task
