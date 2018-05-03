import unittest
import json
import glob
import os

class TestJobOutput(unittest.TestCase):

    def test_allLookupsExist(self):
        '''
        Todo: Use Boto3 to connect to S3 and validate parquet files exists
        '''
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()




