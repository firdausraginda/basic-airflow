# Run Airflow in Docker

## Source:

Basically, this initialization step follows airflow documentation [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).
The summary can do as follows:

1. Create docker-compose.yaml using linux CLI

`$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.1/docker-compose.yaml'`

2. Create folder dags, logs, and plugins in your root directory

`$ mkdir ./dags ./logs ./plugins`

3. Make sure the container and host computer have matching file permissions

`$ echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`

4. Run database migrations and create the first user account

`$ docker-compose up airflow-init`

5. Finally, run the airflow via `docker desktop` app or run this command on CLI

`$ docker-compose up`

6. Airflow webserver can be accessed via `localhost:8080`

-------------

## Airflow Account

By default, both the **username** & **password** for airflow account is `airflow`

-------------

### Add Connection for FileSensor DAG
Need to add new connection with following params to make the FileSensor DAG works:

| Field | Value |
| ------ | ------ |
| Conn Id | my_file_system |
| Conn Type | File (path) |
| Extra | ```{"path": "/opt/airflow/dags/python_operator"}``` |
| Login | `<username>` |
| Password | `<Password>` |

-------------

### Bash Operator, Python Operator, Sensor
This repository contains a few DAGs type, select DAG tag `explore-airflow` to show the following DAGs only:

| No | Type | File Name | Desc |
| ------ | ------ | ------ | ------ |
| 1 | bash operator | `simple_bash_operator.py` | contains 2 tasks, simply echoing string. The 2nd task dependent on the 1st task |
| 2 | bash operator | `templated_bash_operator.py` | using jinja template to loop over files and output the file contents |
| 3 | python operator | `simple_python_operator.py` | print out string from python callable function with specified argument |
| 4 | python operator | `write_file_python_operator.py` | write a json file contains data fetched from URL if URL is provided, or a text file if not |
| 5 | branch python operator | `branch_python_operator.py` | determine which task to run using branch python operator |
| 6 | external sensor | `external_sensor.py` | only run a task after task `write_studio_ghibli_data_task` from `write_file_python_operator` DAG already run first. Run repeatedly, wait 2 minutes between checks |
| 7 | file sensor | `file_sensor.py` | check if a file already exist inside a directory before run a task |
