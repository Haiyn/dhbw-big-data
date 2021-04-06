FROM marcelmittelstaedt/airflow:latest
# Install dependencies
USER airflow
RUN pip3 install pymongo

# Return to root user
USER root
WORKDIR /