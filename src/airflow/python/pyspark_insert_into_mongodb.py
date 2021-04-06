import pyspark
import os, json
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark import SparkContext
import argparse
from pyspark.sql.functions import desc

def get_args():
    """
    Parses Command Line Args
    """
    parser = argparse.ArgumentParser(description='For importing partitioned MTG card data into MongoDB.')
    parser.add_argument('--hdfs_import_dir', help='The HDFS directory where the files to import are located', required=True, type=str)
    parser.add_argument('--hdfs_target_format', help='The files extension of the files that should be imported', required=True, type=str)
    parser.add_argument('--collection', help='The name of the MongoDB collection', required=True, type=str)
    parser.add_argument('--uri', help='The connection string of the MongoDB', required=True, type=str)
    parser.add_argument('--db', help='The database name of the MongoDB', required=True, type=str)

    return parser.parse_args()

if __name__ == '__main__':
    """
    Reads final card data and inserts it into mongodb
    """

    # Parse Command Line Args
    args = get_args()

    # Initialize Spark Context
    sc = pyspark.SparkContext()
    spark = SparkSession(sc)

    # Start the mongo connection
    client = MongoClient(args.uri)
    db = client[args.db]
    cards_collection = db[args.collection]

    # Load all json files from hdfs into df
    cards_dataframe = spark.read.format('json')\
        .load(args.hdfs_import_dir + '/*.' + args.hdfs_target_format)

    # Convert df into json object and insert it into mongodb
    cards = cards_dataframe.toJSON().map(lambda j: json.loads(j)).collect()
    cards_collection.insert_many(cards)

    client.close()