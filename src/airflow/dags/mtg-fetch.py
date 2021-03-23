from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_download_operations import HttpDownloadOperator
from airflow.operators.hdfs_operations import HdfsPutFileOperator, HdfsGetFileOperator, HdfsMkdirFileOperator
from airflow.operators.filesystem_operations import CreateDirectoryOperator
from airflow.operators.filesystem_operations import ClearDirectoryOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.providers.mongo.hooks.mongo import MongoHook

args = {
    'owner': 'airflow'
}

# Create the hive table
hiveSQL_create_table_mtg_cards='''
CREATE EXTERNAL TABLE IF NOT EXISTS mtg_cards(
	id STRING
) COMMENT 'IMDb Ratings' PARTITIONED BY (partition_year int, partition_month int, partition_day int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\t' STORED AS TEXTFILE LOCATION '/user/hadoop/imdb/title_ratings'
TBLPROPERTIES ('skip.header.line.count'='1');
'''

# Create the hive partition table
hiveSQL_add_partition_mtg_cards='''
ALTER TABLE mtg_cards
'''

# Define DAG
dag = DAG('MTG Card Fetch', default_args=args, description='Fetches all up-to-date MTG cards',
          schedule_interval='56 18 * * *',
          start_date=datetime(2019, 10, 16), catchup=False, max_active_runs=1)

# Prepare import directory
create_local_import_dir = CreateDirectoryOperator(
    task_id='create_import_dir',
    path='/home/airflow',
    directory='mtg',
    dag=dag,
)
clear_local_import_dir = ClearDirectoryOperator(
    task_id='clear_import_dir',
    directory='/home/airflow/mtg',
    pattern='*',
    dag=dag,
)

# Fetch data from API
download_title_ratings = HttpDownloadOperator(
    task_id='download_title_ratings',
    download_uri='https://datasets.imdbws.com/title.ratings.tsv.gz',
    save_to='/home/airflow/imdb/title.ratings_{{ ds }}.tsv.gz',
    dag=dag,
)

# Create HDFS directory
create_hdfs_mtg_cards_partition_dir = HdfsMkdirFileOperator(
    task_id='mkdir_hdfs_mtg_cards_dir',
    directory='/user/hadoop/mtg/cards/[PARTITION CRITERIA]',
    hdfs_conn_id='hdfs',
    dag=dag,
)

# Put data into HDFS
hdfs_put_mtg_cards = HdfsPutFileOperator(
    task_id='upload_mtg_cards_to_hdfs',
    local_file='/home/airflow/imdb/[FILE]',
    remote_file='/user/hadoop/imdb/title_ratings/[FILE]',
    hdfs_conn_id='hdfs',
    dag=dag,
)

# Create hive table
create_HiveTable_mtg_cards = HiveOperator(
    task_id='create_mtg_cards',
    hql=hiveSQL_create_table_title_ratings,
    hive_cli_conn_id='beeline',
    dag=dag
)

# Create partitioned table
addPartition_HiveTable_title_ratings = HiveOperator(
    task_id='add_partition_mtg_cards',
    hql=hiveSQL_add_partition_mtg_cards,
    hive_cli_conn_id='beeline',
    dag=dag
)

# Connect to mongodb
connect_MongoDb = MongoHook(
    conn_id:
)

# Put into mongodb
dummy_op = DummyOperator(
        task_id='dummy',
        dag=dag
)

create_local_import_dir >> clear_local_import_dir >> download_mtg_cards >> create_hdfs_mtg_cards_partition_dir >>
hdfs_put_mtg_cards >> create_HiveTable_mtg_cards >> addPartition_HiveTable_mtg_cards >> connect_MongoDb >> dummy_op
