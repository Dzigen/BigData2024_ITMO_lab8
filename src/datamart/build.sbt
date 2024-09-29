ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.19"

lazy val root = (project in file("."))
  .settings(
    name := "datamart"
  )

// Updated syntax
fork := true
javaOptions += "--add-exports=java.base/sun.nio.ch=ALL-UNNAMED"

val sparkVersion = "3.5.1"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.apache.spark" %% "spark-mllib" % sparkVersion,
  "com.typesafe.scala-logging" %% "scala-logging" % "3.9.3",
  "io.circe" %% "circe-core" % "0.14.1",
  "io.circe" %% "circe-generic" % "0.14.1", // For automatic derivation of encoders and decoders
  "io.circe" %% "circe-parser" % "0.14.1"
)

// Add the repository for the Oracle JDBC driver
resolvers ++= Seq(
  "Akka Repository" at "https://repo.akka.io/releases/",
  "Apache Repository" at "https://repo1.maven.org/maven2/",
  //"Oracle Maven Repository" at "https://maven.oracle.com"
)