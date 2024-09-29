package db
import org.apache.spark.sql.{DataFrame, SparkSession}
import com.typesafe.scalalogging.Logger

class MySQLConnector(spark: SparkSession) {
  private val HOST = "mysql-service"
  private val PORT = 3306
  private val DATABASE = "dataset"
  private val JDBC_URL = s"jdbc:mysql://$HOST:$PORT/$DATABASE"
  private val USER = "root"
  private val PASSWORD = "password"

  private val logger = Logger("Logger")

  def read(table: String): DataFrame = {
    logger.info("Чтение датасета из таблицы БД")
    spark.read
      .format("jdbc")
      .option("url", JDBC_URL)
      .option("user", USER)
      .option("password", PASSWORD)
      .option("dbtable", table)
      .option("inferSchema", "true")
      .load()
  }

  def write(df: DataFrame, table: String): Unit = {
    logger.info("Добавление новой записи в таблицу БД")
    df.write
      .format("jdbc")
      .option("url", JDBC_URL)
      .option("user", USER)
      .option("password", PASSWORD)
      .option("dbtable", table)
      .mode("append")
      .save()   
  }
}