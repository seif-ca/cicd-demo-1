import unittest

class TestEtlResults(unittest.TestCase):
        
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


