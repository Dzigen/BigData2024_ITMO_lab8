import configparser
from pyspark.sql import SparkSession
import os
import time
import shutil

from src import Logger, KMeansConnector, MySQLConnectorConfig, MySQLConnector, init_database

CONFIG_PATH = '/configs/config.ini'

print(os.listdir("/configs"))

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

init_database(config, dataset_dir='/data')

JARS = ','.join([f"{config['jars']['jars_dir']}/{jar_file}" for jar_file in 
        [config['jars']['mysql_jar'], config['jars']['datamart_jar'], 
         config['jars']['logging_jar']]])

DB_CONNECTOR_JAR = f"{config['jars']['jars_dir']}/{config['jars']['mysql_jar']}"

spark = SparkSession.builder \
    .appName(config['spark']['app_name']) \
    .master(config['spark']['deploy_mode']) \
    .config("spark.driver.cores", config['spark']['driver_cores']) \
    .config("spark.executor.cores", config['spark']['executor_cores']) \
    .config("spark.driver.memory", config['spark']['driver_memory']) \
    .config("spark.executor.memory", config['spark']['executor_memory']) \
    .config("spark.dynamicAllocation.enabled", config['spark']['dynamic_allocation']) \
    .config("spark.dynamicAllocation.minExecutors", config['spark']['min_executors']) \
    .config("spark.dynamicAllocation.maxExecutors", config['spark']['max_executors']) \
    .config("spark.dynamicAllocation.initialExecutors", config['spark']['initial_executors']) \
    .config("spark.jars", JARS) \
    .config("spark.driver.extraClassPath", DB_CONNECTOR_JAR) \
    .config("spark.executor.extraClassPath", DB_CONNECTOR_JAR) \
    .getOrCreate()

logger = Logger(True).get_logger("logger")
db_config = MySQLConnectorConfig(**dict(config['mysql']))
db_conn = MySQLConnector(spark, logger, db_config)
model = KMeansConnector(2, 'scaled_features', logger, db_conn)

while True:

    while True:
        logger.info("Ожидаем новых данных от DataMart-сервиса")
        if os.path.isdir(config['dataset']['parquet_path']):
            logger.info("Появились данные на обработку!")
            transformed_data = spark.read.parquet(config['dataset']['parquet_path'])
            break
        time.sleep(10)

    model.fit(transformed_data)
    predictions = model.predict(transformed_data)
    scores = model.evaluate(predictions)

    logger.info(f"Score: {scores}")
    time.sleep(10)