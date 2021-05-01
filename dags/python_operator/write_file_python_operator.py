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

def fetch_and_write(path_to_write, url=None):
    """
    write a json file contains data fetched from URL if URL is provided, or a text file if not
    """

    if url:
        response = requests.get(url)

        # create context manager, and set the path relative to this file
        with open(os.path.join(os.path.dirname(__file__), path_to_write), 'wb') as file:
            file.write(response.content)
        print(f'Success fetch data from {url} and write to {path_to_write}')
    
    else:
        with open(os.path.join(os.path.dirname(__file__), path_to_write), 'w') as file:
            file.write(f'execution date: {datetime.now()}')
        print(f'Success write the execution date to {path_to_write}')

with DAG(
    # Define DAG id
    'write_file_python_operator',
    default_args=default_args,
    description='write a json/txt file',
    tags=['explore-airflow'],
    # To enabled/disabled backfilling, set the catchup property
    catchup=False,
    # schedule interval every 2 minutes
    schedule_interval='*/2 * * * *'
) as dag:

    write_todo_list_data = PythonOperator(
        task_id='write_todo_list_data_task',
        python_callable=fetch_and_write,
        op_kwargs={'url': 'http://jsonplaceholder.typicode.com/todos',
            'path_to_write': 'todo.json'},
        dag=dag
    )

    write_studio_ghibli_data = PythonOperator(
        task_id='write_studio_ghibli_data_task',
        python_callable=fetch_and_write,
        op_kwargs={'url': 'https://ghibliapi.herokuapp.com/films/',
            'path_to_write': 'studio_ghibli.json'},
        dag=dag
    )

    write_execution_time = PythonOperator(
        task_id='write_execution_time_task',
        python_callable=fetch_and_write,
        op_kwargs={'path_to_write': 'exec_time.txt'},
        dag=dag
    )

    # Define task depedencies
    write_todo_list_data
    write_execution_time
    write_studio_ghibli_data