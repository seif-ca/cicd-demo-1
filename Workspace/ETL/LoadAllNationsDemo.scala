// Databricks notebook source
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

/* this is a test */

/* this is another test */
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

joinedDf.createOrReplaceTempView("V_ALL_NATIONS")
// this is a test
// This is a demo

// COMMAND ----------

val allNations = sqlContext.sql("SELECT * from V_ALL_NATIONS v JOIN iso_country_codes i on upper(v.NationName) = upper(i.name)")
 display(allNations) 

// COMMAND ----------

allNations.write.csv("/tmp/foo.csv")