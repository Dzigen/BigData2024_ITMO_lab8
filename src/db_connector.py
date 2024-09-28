import pandas as pd
from dataclasses import dataclass, field
from .logger import Logger

@dataclass
class MySQLConnectorConfig:
    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "dataset"
    username: str = "root"
    password: str = "password"
    samples_table: str = "samples"
    predictions_table: str = "predictions"

class MySQLConnector:
    def __init__(self, spark, logger, config: MySQLConnectorConfig = MySQLConnectorConfig()):
        self.config = config        
        self.jdbcUrl = f"jdbc:mysql://{config.host}:{config.port}/{config.database}"
        self.spark = spark
        self.log = logger
    
    @Logger.cls_se_log("Чтение датасета из таблицы БД")
    def read(self, table: str):
        return self.spark.read \
            .format("jdbc") \
            .option("url", self.jdbcUrl) \
            .option("user", self.config.username) \
            .option("password", self.config.password) \
            .option("dbtable", table) \
            .option("inferSchema", "true") \
            .load()
    
    @Logger.cls_se_log("Добавление новой записи в таблицу БД")
    def write(self, df, table: str) -> None:
        df.write \
            .format("jdbc") \
            .option("url", self.jdbcUrl) \
            .option("user", self.config.username) \
            .option("password", self.config.password) \
            .option("dbtable", table) \
            .mode("append") \
            .save()