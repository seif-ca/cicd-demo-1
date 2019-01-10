# Databricks notebook source
# MAGIC %sh
# MAGIC pip install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o --trusted-host h2o-release.s3.amazonaws.com

# COMMAND ----------

import h2o
import pandas as pd
import numpy as np

# COMMAND ----------

h2o.init(max_mem_size = "2G")