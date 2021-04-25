# Run Airflow in Docker

## Source: 
[Airflow Official Docs](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

## How to use:
```docker-compose up```

## How to run the CLI Commands:
```docker-compose run airflow-worker airflow info```

-------------

### Running a Workflow in Airflow
```airflow run <dag-id> <task-id> <start-date>```