# Databricks notebook source
# MAGIC %md
# MAGIC ## Install chrome browser to perform headless browser operations using Selenium
# MAGIC 
# MAGIC 1. Install dependencies
# MAGIC 2. Install Chrome browser
# MAGIC 3. Install Chrome web driver for Selenium

# COMMAND ----------

# MAGIC %sh apt-get install software-properties-common

# COMMAND ----------

# MAGIC %sh add-apt-repository ppa:canonical-chromium-builds/stage

# COMMAND ----------

# MAGIC %sh apt-get update

# COMMAND ----------

# MAGIC %sh apt-get install -y chromium-browser

# COMMAND ----------

# MAGIC %sh which chromium-browser

# COMMAND ----------

# MAGIC %sh wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip

# COMMAND ----------

# MAGIC %sh unzip chromedriver_linux64.zip

# COMMAND ----------

# MAGIC %sh mv chromedriver /usr/bin

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ## Use Selenium library to run google search
# MAGIC 
# MAGIC 1. Install Selenium library using Databricks PyPi library loader
# MAGIC 2. Open session to google.com
# MAGIC 3. Pass search term and submit using driver to interact with HTML form element
# MAGIC 4. Use BeautifulSoup HTML parser to extract results
# MAGIC 5. Create dataframe using results

# COMMAND ----------

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pyspark.sql import Row
import time
import datetime

now = datetime.datetime.now()
now_truncated = datetime.date(now.year, now.month, now.day)

 
class Search:
    def __init__(self, search):
        self.url = 'https://www.google.com/'
        self.setup_browser(self.url)
        self.search = search
        self.exec_search()
        self.results = []
        self.get_results()
         
    def get_results(self):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        divs = soup.find_all('div', {'class':'g'})
        for div in divs:
            desc = div.find('span', {'class':'st'})
            if(desc): 
              descTxt = desc.text
            else:
              descTxt = "Unspecified"
              
            self.results.append(Row(title=div.a.text, url=div.a['href'], description=descTxt, crawldate=now_truncated))
                               
    def exec_search(self):
        self.browser.find_element_by_xpath('//*[@id="lst-ib"]').click()
        self.browser.find_element_by_id("lst-ib").send_keys(self.search)
        time.sleep(1)
        self.browser.find_element_by_name('btnK').submit()
        time.sleep(1)
         
    def setup_browser(self, url):
      options = Options()
      options.add_argument("--headless") # Runs Chrome in headless mode.
      options.add_argument('--no-sandbox') # # Bypass OS security model
      options.add_argument('start-maximized')
      options.add_argument('disable-infobars')
      options.add_argument("--disable-extensions")
      self.browser = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver') 
      self.browser.get(self.url)
 
searchresult = Search('spark')
searchresult.browser.quit()
df = sc.parallelize(searchresult.results).toDF()

# COMMAND ----------

# MAGIC %md
# MAGIC # Persist data in S3
# MAGIC 
# MAGIC You can write your data to a mounted S3 directory

# COMMAND ----------

# or write to a parquet file
#  this data is written to /dbfs/SEARCHES directory
#  you can even overwrite a specific parition to update 
df.write.mode('overwrite').partitionBy("crawldate").parquet("/SEARCHES")
allsearches = spark.read.option("header","true").parquet("/SEARCHES")
display(allsearches)

# COMMAND ----------

# MAGIC %sh ls /dbfs/SEARCHES

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC # Databases and Tables
# MAGIC Tables are a simple way to make structured data available across your organization. Tables are equivalent to Apache Spark DataFrames. This means that you can cache, filter, and perform any operations supported by DataFrames on tables. You can create a table using the Create Table UI or programmatically. You can query tables with Spark APIs and Spark SQL.
# MAGIC 
# MAGIC Databricks uses the Hive metastore to manage tables, and supports all file formats and Hive data sources.  We use the Hive metastore to provide a catalog where our users can store metadata about their databases, tables, views, UDFs, etc. In addition to user-inputted data, Spark stores internal information like the partitions of a table in the metastore.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a global table
# MAGIC Databricks registers global tables to the Hive metastore and makes them available across all clusters.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS SEARCH;

# COMMAND ----------

allsearches.write.saveAsTable("SEARCH")
tblresults = spark.table("SEARCH")
display(tblresults)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Create a local table
# MAGIC You can create a local table on a cluster that is not accessible from other clusters and is not registered in the Hive metastore. This is also known as a temporary table or a view.

# COMMAND ----------

# Create a temp view
resultsFiltered = allsearches.select("title", "url").filter("description = 'Unspecified'")
resultsFiltered.createOrReplaceTempView("V_TMP_SEARCH")
links = spark.table("V_TMP_SEARCH")
display(links)