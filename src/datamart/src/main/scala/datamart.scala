import org.apache.spark.sql.{DataFrame, SparkSession, SaveMode}
import preprocess.{Preprocessor}
import db.{MySQLConnector}
import com.typesafe.scalalogging.Logger

object DataMart {
  private val USER = "root"
  private val PASSWORD = "password"
  private val APP_NAME = "Clustering"
  private val DEPLOY_MODE = "local"
  private val DRIVER_MEMORY = "2g"
  private val EXECUTOR_MEMORY = "2g"
  private val EXECUTOR_CORES = 1
  private val DRIVER_CORES = 1
  private val MYSQL_CONNECTOR_JAR = "/opt/spark/jars/mysql-connector-j-8.4.0.jar"
  private val PARQUET_PATH = "/shared/parquet_openfoodfacts.parquet"
  private val DYNAMIC_ALLOCATION = false
  private val MIN_EXECUTORS = 1
  private val MAX_EXECUTORS = 5
  private val INITIAL_EXECUTORS = 2

  val session = SparkSession.builder
    .appName(APP_NAME)
    .master(DEPLOY_MODE)
    .config("spark.driver.cores", DRIVER_CORES)
    .config("spark.executor.cores", EXECUTOR_CORES)
    .config("spark.driver.memory", DRIVER_MEMORY)
    .config("spark.executor.memory", EXECUTOR_MEMORY)
    .config("spark.dynamicAllocation.enabled", DYNAMIC_ALLOCATION)
    .config("spark.dynamicAllocation.minExecutors", MIN_EXECUTORS)
    .config("spark.dynamicAllocation.maxExecutors", MAX_EXECUTORS)
    .config("spark.dynamicAllocation.initialExecutors", INITIAL_EXECUTORS)
    .config("spark.jars", MYSQL_CONNECTOR_JAR)
    .config("spark.driver.extraClassPath", MYSQL_CONNECTOR_JAR)
    .config("spark.executor.extraClassPath", MYSQL_CONNECTOR_JAR)
    .getOrCreate()

  private val db = new MySQLConnector(session)
  private val logger = Logger("Logger")

  def main(args: Array[String]): Unit = {
    while (true) {
      val transformed = read_transform_dataset()
      transformed.write.mode(SaveMode.Overwrite).parquet(PARQUET_PATH)
      Thread.sleep(10000)
    }
  }

  def read_transform_dataset(): DataFrame = {
    val data = db.read("samples")
    logger.info("OpenFoodFacts-датасет загружен успешно!")

    logger.info("Применение трансформаций к даатсету...")
    val transforms: Seq[DataFrame => DataFrame] = Seq(
      Preprocessor.assemble,
      Preprocessor.apply_scale
    )
    val transformed = transforms.foldLeft(data) { (df, f) => f(df) }
    logger.info("Все трансформации были применены успешно!")
    
    transformed
  }

  def write_predictions(df: DataFrame): Unit = {
    logger.info("Запись предсказаний модели в БД...")
    db.write(df, "predictions")
    logger.info("Все предсказания модели были сохранены в БД успешно!")
  }
}