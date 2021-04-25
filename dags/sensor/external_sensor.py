# Import DAG object
from airflow.models import DAG
# Import the ExternalTaskSensor
from airflow.sensors.external_task_sensor import ExternalTaskSensor
# Import the DummyOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Define the default_args dictionary
default_args = {
  'owner': 'airflow',
  'start_date': datetime(year=2021, month=1, day=1),
  'retries': 2
}

with DAG(
    # Define DAG id
    'external_sensor_dag',
    default_args=default_args,
    description='check if a task from other DAG already run',
    tags=['explore-airflow'],
    # To enabled/disabled backfilling, set the catchup property
    catchup=False,
    schedule_interval='* * * * *'
) as dag:

    external_sensor = ExternalTaskSensor(
        task_id='external_sensor_task',
        # by default mode set to 'poke', which means run repeatedly
        mode='poke',
        # time to wait before the task fail
        timeout=600,
        external_dag_id='write_file_python_operator',
        external_task_id='fetch_and_write_a_file_task',
        dag=dag
    )

    last_task = DummyOperator(task_id='last_task')

    external_sensor >> last_task