# dhbw-big-data-airflow
> An Airflow ETL that uses DAGs to fetch, transform and save MTG card data.

## Structure
> The folder structure of the Airflow component.

- [`/dags`](/src/airflow/dags) contains all used Airflow DAGs.
- [`/plugins`](/src/airflow/plugins) contains all modified plugins (operators, hooks,...) that differ from the operators 
already defined in the docker image `marcelmittelstaedt/spark_base:latest`.
- [`/python`](/src/airflow/python) contains all external python scripts that are used in the DAG(s).
  
## Initialization & Deployment
Airflow runs in a docker container that is started by the [`docker-compose.yml` file](/docker-compose.yml). 

To make all local DAGs, plugins and python scripts available in the container, run the `setup.sh` bash script. 

```bash
sh setup.sh
```

It contains docker copy instructions that by default copy all DAGs in `/src/airflow/dags` and all scripts in 
`/src/airflow/python` to `/home/airflow/airflow/dags` and `/home/airflow/airflow/python` respectively. Plugins must be
copied manually for each file to avoid overwriting existing plugins.

## Workflow
> An overview of the complete ETL process in Airflow.

The complete ETL workflow can be seen in the graphic below.

![Workflow](/docs/workflow.png)

Every job in this workflow is explained in the following section.

## Tasks/Jobs & Transformations
> An overview of each task/job and data transformation in the Airflow DAG.
### 1. create_import_dir
###### Run duration: <3s

Creates the import directory `/home/airflow/mtg` that will store the raw downloaded data.

Uses the bash operator `CreateDirectoryOperator` present in `marcelmittelstaedt/airflow:latest`.

### 2. clear_import_dir
###### Run duration: <3s

Deletes existing data in the import directory.

Uses the bash operator `ClearDirectoryOperator` present in `marcelmittelstaedt/airflow:latest`.


### 3. download_mtg_cards
###### Run duration: ~7m

Downloads all available cards from the MTG API at `https://api.magicthegathering.io/v1/cards/`.

Uses a modified version of the base operator `HttpDownloadOperator` present in `marcelmittelstaedt/airflow:latest`.

Modifications include an iterating integer that represents the page number for the API URL. After every call to
`https://api.magicthegathering.io/v1/cards?page=[page_num]` the integer `page_num` iterates by 1 until the response does
not contain any cards anymore. The maximum page number as of the creation of this project is 566.

#### Downloading automatically

Every fetched page is saved into a python array and written to a single JSON file after the last call. There is room for
performance improvements here:
- Run time could be reduced by running multiple HttpDownloadOperators in different page ranges in parallel (e.g. 6 
  Operators, each downloading 100 pages)
- Write times can be improved by saving the results to multiple JSON files instead of one big JSON file

The results of the download operation is found in `/home/airflow/mtg/raw.json`.


### Downloading manually

`/src/airflow/plugins/operators` includes a test file (`http_download_operator_test.py`) that lets you run the script 
locally. To run it, simply type following command into the bash at the file location of the test script:

```bash
python3 http_download_operator_test.py
```

The resulting file will be saved in the same directory where the test script is located.

### 4. mkdir_hdfs_mtg_cards_dir
###### Run duration: ~5s

Creates a directory for the raw data on the Hadoop File System at `/user/hadoop/mtg/cards/[year]/[month]/[day]` whereas
the parameters are replaced by the execution year/month/day.

Uses the base operator `HdfsMkdirFileOperator` present in `marcelmittelstaedt/airflow:latest`.


### 5. upload_mtg_cards_to_hdfs
###### Run duration: ~5s

Put the downloaded JSON file into the created HDFS directory.

Uses the base operator `HdfsPutFileOperator` present in `marcelmittelstaedt/airflow:latest`.


### 6. pyspark_create_final_mtg_cards
###### Run duration: ~2m

Reads the data from the Hadoop file system and transforms it.

Uses the PySpark submit operator with the python script `pyspark_format_mtg_cards` present in `src/airflow/python`.

The submit operator is parameterized with all file locations (source and target), file format as well as execution year,
month and day.
Duplicates do not need to be dropped. There are duplicate card names but they are from different MTG sets and thus have
varying descriptions, artists and/or artwork. 

Only the needed properties `mutliverseid`, `name`, `artist` and `text` are saved. The image URL for the card itself can
be constructed with the multiverseid and the following URL: 
`http://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid=[multiverseid]`. All data is sorted descending
by the multiverseid. 

### 7. pyspark_import_into_mongodb
###### Run duration: ~10s

Reads the data from the Hadoop file system and bulk inserts it into the MongoDB.

Uses the PySpark submit operator with the python script `pyspark_insert_into_mongodb` present in `src/airflow/python`.

#### Importing automatically
The final json data is a pure JSON array populated with JSON elements that contain the multiverse ID, name, artist and 
text of each card. It is imported via a PySpark script from HDFS to the MongoDB.

The PySpark submit operator is called with following parameters:
- `hdfs_import_dir` The directory that should be scanned for importable files
- `hdfs_target_format` The file format (extension) of the files that should be imported
- `uri` The MongoDB connection string
- `db` The name of the MongoDB database to import the data to
- `collection` The name of the collection in the MongoDB to import the data into

The script can be found in `/src/airflow/python/pyspark_insert_into_mongodb.py`.
It loads all JSON files from the final HDFS save location defined by the mtg-fetch DAG. It then uses the python package 
`pymongo` to run a bulk insert on the PySpark dataframe. In order to make the python package available, it needs to be 
installed for the hadoop user in the container. This is achieved by modifying the Airflow Dockerfile at 
`/src/airflow/Dockerfile`.

This script will run automatically in the context of the Airflow ETL DAG.

#### Importing manually
You may import data manually from the hadoop container. Please be aware that you will need the package `mongo-tools` for 
this. It can be installed via `sudo apt install mongo-tools`.

To test it locally, use
```bash
mongoimport --jsonArray --uri "mongodb://dev:dev@127.0.0.1:27017/dhbw-big-data-mongodb" --collection Cards --file [filepath]
```

Replace `[filepath]` with the path to the file you want to import. An example json with 3 entries is available in 
`/src/mongodb/sample_data.json`.

Replace the localhost IP address with the container
if you're running the command from within a docker container.

The command in the DAG includes two more arguments to ensure smooth processing of large data:
- `--batchSize 100` defines a smaller batch size (default is 10000)
- `--numInsertionWorkers 310` defines how many workers should insert at the same time (you can set this value to whatever
  you want)
