import unittest
import json
import glob
import os


class TestJobOutput(unittest.TestCase):

    test_output_path = '#ENV#'


    def test_performance(self):
        path = self.test_output_path
        statuses = []

        for filename in glob.glob(os.path.join(path, '*.json')):
            print('Evaluating: ' + filename)
            data = json.load(open(filename))
            duration = data['execution_duration']
            if duration > 100000:
                status = 'FAILED'
            else:
                status = 'SUCCESS'

            statuses.append(status)

        self.assertFalse('FAILED' in statuses)

    def test_job_run(self):
        path = self.test_output_path
        statuses = []

        for filename in glob.glob(os.path.join(path, '*.json')):
            print('Evaluating: ' + filename)
            data = json.load(open(filename))
            status = data['state']['result_state']
            statuses.append(status)

        self.assertFalse('FAILED' in statuses)
        
    def getSimilarProds(self):
        # connect to shard using dbconnect
        spark = SparkSession\
                .builder\
                .getOrCreate()

        # The Spark code will execute on the Databricks cluster.
        df = spark.sql("select * from product_similarity")

        dfcnt = df.where(df['similarity_score'] > .5)

        return dfcnt.count()

    def test_SimilarProds(self):

        val = self.getSimilarProds()
        print(val)
        self.assertGreater(val, 1, "Bad")        

        
if __name__ == '__main__':
    unittest.main()




