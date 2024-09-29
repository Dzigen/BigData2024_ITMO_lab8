FROM sbtscala/scala-sbt:eclipse-temurin-17.0.4_1.7.1_3.2.0

WORKDIR /app
COPY . /app/.

COPY ./lib/mysql-connector-j-8.4.0.jar /opt/spark/jars/mysql-connector-j-8.4.0.jar
COPY ./lib/scala-logging_2.12-3.9.3.jar /opt/spark/jars/scala-logging_2.12-3.9.3.jar

COPY ./datamart_libs /root

ENTRYPOINT ["sbt", "runMain DataMart"]