// Databricks notebook source
import org.apache.spark.sql.Encoders

case class Supplier(SuppKey: Int, Name: String, Address: String, NationKey: Int,
                    Phone: String, AcctBal: Double,
                    Comment: String)

var suppSchema = Encoders.product[Supplier].schema

val suppDf = sqlContext.read
         .format("csv")
         .option("header", "false") //reading the headers
         .schema(suppSchema)
         .option("delimiter", "|")
         .load("/databricks-datasets/tpch/data-001/supplier/")

suppDf.createOrReplaceTempView("V_SUPPLIERS")

/*
this is a test
*/

display(suppDf)