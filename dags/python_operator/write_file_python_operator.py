# Import DAG object
from airflow.models import DAG
# Import the PythonOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
import os

# Define the default_args dictionary
default_args = {
  'owner': 'airflow',
  'start_date': datetime(year=2021, month=1, day=1),
  'retries': 2,
}

def fetch_and_write(url, path_to_write):
    """
    fetch data from url then write to a json file
    """
    response = requests.get(url)
    # create context manager, and set the path relative to this file
    with open(os.path.join(os.path.dirname(__file__), path_to_write), 'wb') as file:
        file.write(response.content)
    print(f'Success fetch data from {url} and write to {path_to_write}')

with DAG(
    # Define DAG id
    'write_file_python_operator',
    default_args=default_args,
    description='write a json file contains data from fetched URL',
    tags=['explore-airflow'],
    # To enabled/disabled backfilling, set the catchup property
    catchup=False,
    schedule_interval='* * * * *'
) as dag:

    fetch_and_write_a_file = PythonOperator(
        task_id='fetch_and_write_a_file_task',
        python_callable=fetch_and_write,
        op_kwargs={'url': 'http://jsonplaceholder.typicode.com/todos',
            'path_to_write': 'todo.json'},
        dag=dag
    )

    # Define task depedencies
    fetch_and_write_a_file