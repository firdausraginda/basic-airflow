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
    'external_sensor',
    default_args=default_args,
    description='check if a task from other DAG already run',
    tags=['explore-airflow', 'sensor'],
    # To enabled/disabled backfilling, set the catchup property
    catchup=False,
    # schedule interval every 2 minutes
    schedule_interval='*/2 * * * *'
) as dag:

    external_sensor = ExternalTaskSensor(
        task_id='external_sensor_task',
        # by default mode set to 'poke', which means run repeatedly
        mode='poke',
        # wait 300 between checks
        poke_interval=300,
        external_dag_id='write_file_python_operator',
        external_task_id='write_studio_ghibli_data_task',
        dag=dag
    )

    last_task = DummyOperator(task_id='last_task')

    external_sensor >> last_task