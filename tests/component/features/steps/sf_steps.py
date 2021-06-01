from airflowbigdataoperators.com.kenshoo.shared_tests.component.features.steps.sf_steps import *
from airflow_bi_shared_components.include.steps.sf_steps import *
from behave import step


@step('[SF] I create under schema {schema_name} the following tables')
def step_create_tables_in_schema(context, schema_name):
    step_create_tables(context,"tests/component/features/steps/queries/{schema_name}".format(schema_name=schema_name))

