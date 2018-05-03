import unittest
import json
import glob
import os

class TestJobOutput(unittest.TestCase):

    test_output_path = '#ENV#'

    def test_job_run(self):
        path = self.test_output_path
        statuses = []

        for filename in glob.glob(os.path.join(path, '*.json')):
            print('Evaluating: ' + filename)
            data = json.load(open(filename))
            status = data['state']['result_state']
            statuses.append(status)

        self.assertFalse('FAILED' in statuses)

if __name__ == '__main__':
    unittest.main()




