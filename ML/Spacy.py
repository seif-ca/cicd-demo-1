# Databricks notebook source
import spacy

nlp = spacy.load('en')

# COMMAND ----------

# MAGIC %sh
# MAGIC /databricks/python/bin/python -m spacy download en

# COMMAND ----------

spacy.load('en')