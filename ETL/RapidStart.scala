// Databricks notebook source
// MAGIC %sql
// MAGIC SHOW tables

// COMMAND ----------

val same_query_as_above = sqlContext.sql("show tables")
display(same_query_as_above)

// COMMAND ----------

val names = sqlContext.sql("select sum(count) as cnt, first_name from tbl_baby_names group by first_name")
names.show()

// COMMAND ----------

// MAGIC %fs ls

// COMMAND ----------

val ls = dbutils.fs.ls("/")
display(ls)

// COMMAND ----------

dbutils.fs.help()

// COMMAND ----------

val sparkDF = spark.read.format("parquet")
.option("header", "true")
.option("inferSchema", "true")
.load("/SEARCHES")

// COMMAND ----------

display(sparkDF)

// COMMAND ----------

import org.apache.spark.sql.Encoders

case class NationSchema(NationKey: Int, Name: String, RegionKey: Int,
                      Comment: String)

var nationSchema = Encoders.product[NationSchema].schema

val nationsDf = sqlContext.read
         .format("csv")
         .option("header", "false") //reading the headers
         .schema(nationSchema)
         .option("delimiter", "|")
         .load("/databricks-datasets/tpch/data-001/nation/")

case class RegionSchema(RegionKey: Int, Name: String, Comment: String)

var regionSchema = Encoders.product[RegionSchema].schema

val regionsDf = sqlContext.read
         .format("csv")
         .option("header", "false") //reading the headers
         .schema(regionSchema)
         .option("delimiter", "|")
         .load("/databricks-datasets/tpch/data-001/region/")

val joinedDf = nationsDf.join(regionsDf, nationsDf("RegionKey") === regionsDf("RegionKey"), "inner")
                        .select(nationsDf("NationKey"), nationsDf("Name").as("NationName"), regionsDf("RegionKey"), regionsDf("Name").as("RegionName"))


joinedDf.write.csv("/tmp/nations.csv")

// COMMAND ----------

// MAGIC %sh wget dbfs:/tmp/rows.json "https://health.data.ny.gov/api/views/jxy9-yhdk/rows.json?accessType=DOWNLOAD"

// COMMAND ----------

// MAGIC %fs ls dbfs:/tmp