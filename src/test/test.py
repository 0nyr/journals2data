# unit tests
#    + doc: https://docs.python.org/3/library/unittest.html 

import unittest

# personal packages
import test_data


tests: unittest.suite.TestSuite = unittest.TestLoader.discover("src/test")

results: unittest.TestResult()

tests.run(results)


if __name__ == '__main__':
    unittest.main()