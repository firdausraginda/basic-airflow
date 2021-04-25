# Run Airflow in Docker

## Source: 
[Airflow Official Docs](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

## How to use:
```docker-compose up```

then open ```localhost:8080```

## How to run thru the CLI Commands:
```docker-compose run airflow-worker airflow info```

-------------

### Add Connection for FileSensor DAG
Need to add new connection with following params to make the FileSensor DAG works:

| Field | Value |
| ------ | ------ |
| Conn Id | my_file_system |
| Conn Type | File (path) |
| Extra | ```{"path": "/opt/airflow/dags/python_operator"}``` |