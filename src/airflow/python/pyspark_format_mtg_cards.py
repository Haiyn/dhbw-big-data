import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
import argparse
from pyspark.sql.functions import desc

def get_args():
    """
    Parses Command Line Args
    """
    parser = argparse.ArgumentParser(description='For partitioned MTG card data storage  within HDFS.')
    parser.add_argument('--year', help='Partion Year To Process, e.g. 2019', required=True, type=str)
    parser.add_argument('--month', help='Partion Month To Process, e.g. 10', required=True, type=str)
    parser.add_argument('--day', help='Partion Day To Process, e.g. 31', required=True, type=str)
    parser.add_argument('--hdfs_source_dir', help='HDFS source directory, e.g. /user/hadoop/mtg/raw', required=True, type=str)
    parser.add_argument('--hdfs_target_dir', help='HDFS target directory, e.g. /user/hadoop/mtg/final', required=True, type=str)
    parser.add_argument('--hdfs_target_format', help='HDFS target format, e.g. csv or parquet or...', required=True, type=str)

    return parser.parse_args()

if __name__ == '__main__':
    """
    Reads & formats raw data from HDFS and writes final data
    """

    # Parse Command Line Args
    args = get_args()

    # Initialize Spark Context
    sc = pyspark.SparkContext()
    spark = SparkSession(sc)

    # Read the raw card json from source directory
    raw_mtg_card_dataframe = spark.read.format('json')\
	    .options(header='true', delimiter=',', nullValue='null', inferschema='true')\
	    .load(args.hdfs_source_dir + '/' + args.year + '/' + args.month + '/' + args.day + '/raw.json')

    # Sanitize and select only the relevant data
    raw_mtg_card_dataframe = raw_mtg_card_dataframe\
        .orderBy(desc('multiverseid'))\
        .select('multiverseid', 'name', 'artist', 'text')

    # Write data to HDFS
    raw_mtg_card_dataframe.write.format('json')\
        .mode('overwrite')\
        .save(args.hdfs_target_dir)