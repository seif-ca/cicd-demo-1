# Databricks notebook source
# MAGIC %fs
# MAGIC ls dbfs:/libs

# COMMAND ----------

# MAGIC %sh
# MAGIC unzip /dbfs/libs/*.zip -d /dbfs/libs

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /dbfs/libs/word2vec-master
# MAGIC ls
# MAGIC make

# COMMAND ----------

