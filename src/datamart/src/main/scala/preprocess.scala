package preprocess
import org.apache.spark.ml.feature.{StandardScaler, VectorAssembler}
import org.apache.spark.sql.{DataFrame, SaveMode}
import com.typesafe.scalalogging.Logger

object Preprocessor {

  private val logger = Logger("Logger")

  def assemble(df: DataFrame): DataFrame = {
    logger.info("Старт приведения экзмепляров в векторный формат...")
    val outputCol = "features"
    val inputCols = "code" :: "created_t" :: "last_modified_t" :: "completeness" :: Nil

    val vector_assembler = new VectorAssembler()
      .setInputCols(df.columns)
      .setOutputCol(outputCol)
      .setHandleInvalid("skip")
    val result = vector_assembler.transform(df)
    logger.info("Экземпляры датасета приведены в векторный формат успешно!")
    result
  }

  def apply_scale(df: DataFrame): DataFrame = {
    logger.info("Старт применения к экземпларам датасета StandardScaler-трансформации")
    val scaler = new StandardScaler()
      .setInputCol("features")
      .setOutputCol("scaled_features")
    val scalerModel = scaler.fit(df)
    val result = scalerModel.transform(df)
    logger.info("Трансформация применена!")
    result
  }
}