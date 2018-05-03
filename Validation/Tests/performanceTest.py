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
                status = 'FAILURE'
            else:
                status = 'SUCCESS'

            statuses.append(status)

        self.assertFalse('FAILURE' in statuses)

if __name__ == '__main__':
    unittest.main()




