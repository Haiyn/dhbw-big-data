# dhbw-big-data-airflow
> An Airflow ETL that uses DAGs to fetch, transform and save MTG card data.

## Structure
> The folder structure of the Airflow component.

- [`/dags`](/src/airflow/dags) contains all used Airflow DAGs.
- [`/plugins`](/src/airflow/plugins) contains all modified plugins (operators, hooks,...) that differ from the operators 
already defined in the docker image `marcelmittelstaedt/spark_base:latest`.
- [`/python`](/src/airflow/python) contains all external python scripts that are used in the DAG(s).
  
## Initialization & Deployment
Airflow runs in a docker container that is started by the [`docker-compose.yml` file](/docker-compose.yml). The compose
file uses volumes to transfer all DAGs, plugins and python script files to the target container.

## Workflow
> An overview of the complete ETL process in Airflow.

## Tasks/Jobs & Transformations
> An overview of each task/job and data transformation in the Airflow DAG.
### Mongo Import
The final json data is a pure JSON array. It is imported via `mongoimport` from the `mongo-tools` package.

To test it locally, use
```bash
mongoimport --jsonArray --uri "mongodb://dev:dev@127.0.0.1:27017/dhbw-big-data-mongodb" --collection Cards --file [filepath]
```

Replace `[filepath]` with the path to the file you want to import. An example json with 3 entries is available in 
[`/src/mongodb/sample_data.json`](/src/mongodb/sample_data.json).

Replace the localhost IP address with the container
if you're running the command from within a docker container.

The command in the DAG includes two more arguments to ensure smooth processing of large data:
- `--batchSize 100` defines a smaller batch size (default is 10000)
- `--numInsertionWorkers 310` defines how many workers should insert at the same time (we chose 310 since we assume ~3100 cards with a batch size of 100)
