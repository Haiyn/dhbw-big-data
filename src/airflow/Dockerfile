FROM marcelmittelstaedt/airflow:latest

# Install mongo-tools, needed for airflow task mongoimport
RUN sudo apt install mongo-tools -y

# Copy all needed data to container
USER airflow
ADD mtg-fetch.py /home/airflow/airflow/dags/
ADD http_download_operator.py /home/airflow/airflow/plugins/operators/http_download_operator.py
ADD pyspark_format_mtg_cards.py /home/airflow/airflow/python/

USER root
WORKDIR /