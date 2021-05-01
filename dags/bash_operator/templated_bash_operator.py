# Import DAG object
from airflow.models import DAG
# Import the BashOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Define the default_args dictionary
default_args = {
  'owner': 'airflow',
  'start_date': datetime(year=2021, month=1, day=1),
  'retries': 2,
}

with DAG(
    # Define DAG id
    'templated_bash_operator',
    default_args=default_args,
    description='read all json file content',
    tags=['explore-airflow', 'bash-operator'],
    # To enabled/disabled backfilling, set the catchup property
    catchup=False,
    schedule_interval='@daily'
) as dag:

    # templated command to read the file's content
    templated_command="""
    "execution date: {{ds}}"
    {% for filename in params.filenames %}
        cat "/opt/airflow/dags/python_operator/{{filename}}"
    {% endfor %}
    """

    # Define the BashOperator
    read_json_file = BashOperator(
        task_id='read_json_file_task',
        # Define the bash_command
        bash_command=templated_command,
        params={'filenames': ['todo.json', 'studio_ghibli.json']},
        dag=dag
    )

    # Define task depedencies
    read_json_file