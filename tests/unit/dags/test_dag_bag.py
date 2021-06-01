from airflow.models import DagBag

NO_DAG_ID = '[]'


class TestDagsCompilation(object):
    @classmethod
    def setup_class(self):
        self.dagbag = DagBag(include_examples=False)

    def test_import_dags(self):
        assert len(self.dagbag.import_errors) == 0, \
            'DAG import failures. Errors: {}'.format(self.dagbag.import_errors)

    def test_duplicate_dag_ids(self):
        dag_ids = [dag.dags for dag in self.dagbag.dagbag_stats if dag.dags != NO_DAG_ID]
        for dag_id in dag_ids:
            assert dag_ids.count(dag_id) == 1, ('DAG id {} is duplicated'
                                                '\n\t Detected from following DAG ids: {}'.format(dag_id, dag_ids))
