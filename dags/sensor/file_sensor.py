# Import DAG object
from airflow.models import DAG
# Import the FileSensor
from airflow.contrib.sensors.file_sensor import FileSensor
# Import the DummyOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime
import os

# Define the default_args dictionary
default_args = {
  'owner': 'airflow',
  'start_date': datetime(year=2021, month=1, day=1),
  'retries': 2,
}

with DAG(
    # Define DAG id
    'file_sensor',
    default_args=default_args,
    description='check if a file is exists inside a dir',
    tags=['explore-airflow', 'sensor'],
    # To enabled/disabled backfilling, set the catchup property
    catchup=False,
    # schedule interval every 6 minutes
    schedule_interval='*/6 * * * *'
) as dag:

    file_sensor = FileSensor(
        task_id='file_sensor_task',
        # the file path has been set in admin -> connection, so just need to specify the file name here
        filepath='todo.json',
        # set the fs_conn_id (admin -> connections)
        fs_conn_id='my_file_system',
        # by default mode set to 'poke', which means run repeatedly
        mode='poke',
        # wait 300 between checks
        poke_interval=300,
        dag=dag
    )

    last_task = DummyOperator(task_id='last_task')

    file_sensor >> last_task