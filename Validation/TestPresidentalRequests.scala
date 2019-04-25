// Databricks notebook source
// %run "../ETL/PresidentialRequests"

// COMMAND ----------

printf("Total Washingtons: %,d%n", washingtons.size )
printf("Total Washington Requests: %,d%n", totalWashingtons)

val expectedCount = 466
assert (washingtons.size == expectedCount, s"Expected ${expectedCount} articles but found ${washingtons.size}")

val expectedTotal = 3266
assert (totalWashingtons == expectedTotal, s"Expected ${expectedTotal} requests but found ${totalWashingtons}")

println("-"*80)

// COMMAND ----------

printf("Total Adams: %,d%n", adams.size )
printf("Total Adams Requests: %,d%n", totalAdams)

val expectedCount = 235
assert (adams.size == expectedCount, s"Expected ${expectedCount} articles but found ${adams.size}")

val expectedTotal = 3126
assert (totalAdams == expectedTotal, s"Expected ${expectedTotal} requests but found ${totalAdams}")

println("-"*80)