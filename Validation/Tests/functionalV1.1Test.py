import unittest
import json
import glob
import os

class TestJobOutput(unittest.TestCase):

    def test_ml_model_accuracy(self):
        '''
        Todo: Use DB REST API to execute validation notebooks with asserts
        '''
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()




