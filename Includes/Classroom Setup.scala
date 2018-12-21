// Databricks notebook source
// MAGIC %python
// MAGIC # This notebook sets up mounts and other utility functions used by all notebooks.
// MAGIC 
// MAGIC # Used to identify a region so that we can [eventually] have region-specific buckets.
// MAGIC # def getRegion():
// MAGIC #   import json
// MAGIC #   import urllib2
// MAGIC #   url="http://169.254.169.254/latest/dynamic/instance-identity/document"
// MAGIC #   response=urllib2.urlopen(url)
// MAGIC #   json = json.load(response)
// MAGIC #   return json["region"]
// MAGIC 
// MAGIC # Mount our data sources
// MAGIC mounts=[
// MAGIC   {
// MAGIC     "mount-point": "/mnt/training",
// MAGIC     "s3-bucket": "databricks-corp-training/common",
// MAGIC     "aws-access-key": "AKIAJBRYNXGHORDHZB4A",
// MAGIC     "aws-secret-key": "a0BzE1bSegfydr3%2FGE3LSPM6uIV5A4hOUfpH8aFF",
// MAGIC   }
// MAGIC ]
// MAGIC existing_mounts = {m.mountPoint: m.source for m in dbutils.fs.mounts()}
// MAGIC for mnt in mounts:
// MAGIC   if mnt["mount-point"] not in existing_mounts:
// MAGIC     dbutils.fs.mount("s3a://{aws-access-key}:{aws-secret-key}@{s3-bucket}".format(**mnt), mnt["mount-point"])
// MAGIC 
// MAGIC     
// MAGIC # Utility method to count & print the number of records in each partition.
// MAGIC from pyspark.sql.functions import *
// MAGIC 
// MAGIC def printRecordsPerPartition(df):
// MAGIC   print("Per-Partition Counts:")
// MAGIC   def countInPartition(iterator): yield __builtin__.sum(1 for _ in iterator)
// MAGIC   results = (df.rdd                   # Convert to an RDD
// MAGIC     .mapPartitions(countInPartition)  # For each partition, count
// MAGIC     .collect()                        # Return the counts to the driver
// MAGIC   )
// MAGIC   # Print out the results.
// MAGIC   for result in results: print("* " + str(result))
// MAGIC   
// MAGIC def assertSparkVersion(expMajor, expMinor):
// MAGIC   major, minor, _ = spark.version.split('.')
// MAGIC   if (int(major) < expMajor) or (int(major) == expMajor and int(minor) < expMinor):
// MAGIC     raise Exception("This notebook must run on Spark "+str(expMajor)+"."+str(expMinor)+" or better.")
// MAGIC     
// MAGIC None # suppress output

// COMMAND ----------

// MAGIC %scala
// MAGIC 
// MAGIC // 2 Scala alternatives for getting the region.
// MAGIC // import com.databricks.backend.daemon.driver.DriverConf
// MAGIC // import com.databricks.conf.trusted.ProjectConf
// MAGIC // import com.databricks.backend.common.util.Project
// MAGIC // val conf = new DriverConf(ProjectConf.loadLocalConfig(Project.Driver))
// MAGIC // conf.region
// MAGIC //
// MAGIC // def getRegion() : String = {
// MAGIC //   import org.json4s._
// MAGIC //   import org.json4s.jackson.JsonMethods._
// MAGIC //   implicit val formats=DefaultFormats
// MAGIC //   val url="http://169.254.169.254/latest/dynamic/instance-identity/document"
// MAGIC //   val responseBody=scala.io.Source.fromURL(url).mkString
// MAGIC //   val json=parse(responseBody)
// MAGIC //   (json \ "region").extract[String]
// MAGIC // }
// MAGIC 
// MAGIC // Make the username available to all other languages.
// MAGIC // "WARNING: use of the "current" username is unpredictable 
// MAGIC // when multiple users are collaborating and should be replaced 
// MAGIC // with the notebook ID instead.
// MAGIC 
// MAGIC val username = com.databricks.logging.AttributionContext.current.tags(com.databricks.logging.BaseTagDefinitions.TAG_USER);
// MAGIC spark.conf.set("com.databricks.training.username", username)
// MAGIC 
// MAGIC // Utility method to count & print the number of records in each partition.
// MAGIC import org.apache.spark.sql.functions._
// MAGIC 
// MAGIC def printRecordsPerPartition(df:org.apache.spark.sql.Dataset[Row]):Unit = {
// MAGIC   println("Per-Partition Counts:")
// MAGIC   val results = df.rdd                                   // Convert to an RDD
// MAGIC     .mapPartitions(it => Array(it.size).iterator, true)  // For each partition, count
// MAGIC     .collect()                                           // Return the counts to the driver
// MAGIC 
// MAGIC   results.foreach(x => println("* " + x))
// MAGIC }
// MAGIC 
// MAGIC def assertSparkVersion(expMajor:Int, expMinor:Int):Unit = {
// MAGIC   val Array(major, minor, _) = spark.version.split("""\.""")
// MAGIC   if ((major.toInt < expMajor) || (major.toInt == expMajor && minor.toInt < expMinor)) 
// MAGIC     throw new Exception(s"This notebook must run on Spark $expMajor.$expMinor or better.")
// MAGIC }
// MAGIC 
// MAGIC displayHTML("All done!<br/><br/>") // suppress output

// COMMAND ----------

// MAGIC %python
// MAGIC 
// MAGIC username = spark.conf.get("com.databricks.training.username")
// MAGIC 
// MAGIC None # suppress output