FROM marcelmittelstaedt/airflow:latest

# Install mongo-tools, needed for airflow task mongoimport
RUN sudo apt install mongo-tools -y

# Copy all needed data to container
COPY ./dags/mtg-fetch.py /home/airflow/airflow/dags/
COPY ./plugins/operators/http_download_operator.py /home/airflow/airflow/plugins/
COPY ./python/pyspark_format_mtg_cards.py /home/airflow/airflow/python/

EXPOSE 8030
EXPOSE 8031
EXPOSE 8032
EXPOSE 8088
EXPOSE 8888
EXPOSE 9000
EXPOSE 9864
EXPOSE 9870
EXPOSE 10000