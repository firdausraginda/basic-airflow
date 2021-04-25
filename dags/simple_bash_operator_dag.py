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
    'bash_operator_dag',
    default_args=default_args,
    # Define description of the DAG
    description='echoing simple string',
    # Define the DAG tag
    tags=['explore-airflow'],
    # To enabled/disabled backfilling
    catchup=False,
    # Define when the dag will triggered
    schedule_interval='@daily'
) as dag:

    # Define the BashOperator 
    first_task = BashOperator(
        task_id='first_task',
        # Define the bash_command
        bash_command='echo "testing first bash operator"',
        # Add the task to the dag
        dag=dag
    )

    # Define the BashOperator 
    second_task = BashOperator(
        task_id='second_task',
        # Define the bash_command
        bash_command='echo "testing second bash operator"',
        # Add the task to the dag
        dag=dag
    )

    first_task >> second_task