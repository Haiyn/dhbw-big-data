#!/bin/bash

# Prepare airflow container
# Copy custom airflow files to destination directories in the airflow container
docker cp ./src/airflow/dags/. airflow:/home/airflow/airflow/dags
docker cp ./src/airflow/plugins/operators/http_download_operator.py airflow:/home/airflow/airflow/plugins/operators/
docker cp ./src/airflow/python/. airflow:/home/airflow/airflow/python

