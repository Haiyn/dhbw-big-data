from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_download_operations import HttpDownloadOperator
from airflow.operators.hdfs_operations import HdfsPutFileOperator, HdfsGetFileOperator, HdfsMkdirFileOperator
from airflow.operators.filesystem_operations import CreateDirectoryOperator
from airflow.operators.filesystem_operations import ClearDirectoryOperator

args = {
    'owner': 'airflow'
}

# Define DAG
dag = DAG('MTG Card Fetch', default_args=args, description='Fetches all up-to-date MTG cards',
          schedule_interval='56 18 * * *',
          start_date=datetime(2019, 10, 16), catchup=False, max_active_runs=1)

# Prepare import directory
create_local_import_dir = CreateDirectoryOperator(
    task_id='create_import_dir',
    path='/home/airflow',
    directory='mtg/raw',
    dag=dag,
)
clear_local_import_dir = ClearDirectoryOperator(
    task_id='clear_import_dir',
    directory='/home/airflow/mtg/raw',
    pattern='*',
    dag=dag,
)

# Fetch data from API
download_title_ratings = HttpDownloadOperator(
    task_id='download_mtg_cards',
    download_uri='https://api.magicthegathering.io/v1/cards',
    save_to='/home/airflow/mtg/raw/raw.json',
    dag=dag,
)

# Create HDFS directory separated by date: y/m/d
create_hdfs_mtg_cards_partition_dir = HdfsMkdirFileOperator(
    task_id='mkdir_hdfs_mtg_cards_dir',
    directory='/user/hadoop/mtg/cards/{{ macros.ds_format(ds, "%Y-%m-%d", "%Y")}}/{{ macros.ds_format(ds, "%Y-%m-%d", "%m")}}/{{ macros.ds_format(ds, "%Y-%m-%d", "%d")}}',
    hdfs_conn_id='hdfs',
    dag=dag,
)

# Put data into HDFS
hdfs_put_mtg_cards = HdfsPutFileOperator(
    task_id='upload_mtg_cards_to_hdfs',
    local_file='/home/airflow/mtg/raw/raw.json',
    remote_file='/user/hadoop/mtg/{{ macros.ds_format(ds, "%Y-%m-%d", "%Y")}}/{{ macros.ds_format(ds, "%Y-%m-%d", "%m")}}/{{ macros.ds_format(ds, "%Y-%m-%d", "%d")}}/raw.json',
    hdfs_conn_id='hdfs',
    dag=dag,
)

pyspark_create_final_mtg_data = SparkSubmitOperator(
    task_id='pyspark_create_final_mtg_data',
    conn_id='spark',
    application='/home/airflow/airflow/python/pyspark_format_mtg_cards.py',
    total_executor_cores='2',
    executor_cores='2',
    executor_memory='2g',
    num_executors='2',
    name='pyspark_create_final_mtg_data',
    verbose=True,
    application_args=['--year', '{{ macros.ds_format(ds, "%Y-%m-%d", "%Y")}}', '--month', '{{ macros.ds_format(ds, "%Y-%m-%d", "%m")}}', '--day',  '{{ macros.ds_format(ds, "%Y-%m-%d", "%d")}}', '--hdfs_source_dir', '/user/hadoop/mtg/raw', '--hdfs_target_dir', '/user/hadoop/mtg/final', '--hdfs_target_format', 'json'],
    dag = dag
)

# Connect to mongodb
insert_into_mongodb = BashOperator(
    task_id='bash_insert_into_mongodb',
    bash_command='/usr/bin/mongo localhost:27017/dhbw-big-data-mongodb -u dev -p dev; data=`cat /user/hadoop/mtg/final/[FILENAME]`; db.Cards.insert_many(data);',
    dag=dag
)

create_local_import_dir >> clear_local_import_dir >> download_mtg_cards >> create_hdfs_mtg_cards_partition_dir >>
hdfs_put_mtg_cards >> pyspark_create_final_mtg_data >> connect_MongoDb >> dummy_op
