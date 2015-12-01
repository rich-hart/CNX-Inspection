import unittest

settings = None


class GeneralTestCase(unittest.TestCase):
    def __init__(self, methodName, param1=None, param2=None):
        test_name = "test_pages ({0},{1})".format(param1,param2)
        setattr(GeneralTestCase, test_name,self.runTest)
        super(GeneralTestCase, self).__init__(test_name)
        self.param1 = param1
        self.param2 = param2

    @classmethod
    def setUpClass(cls):
        global settings
        cls.settings = settings         

    def setUp(self):
#        import ipdb; ipdb.set_trace()
        pass #print("\nsetUp: setup up {0} {1}".format(self.param1,self.param2))

    def runTest(self):
        pass #print("\nrunTest: testing {0} {1}".format(self.param1,self.param2)) # Test that depends on param 1 and 2.

    def tearDown(self):
        pass #print("\ntearDown: tear down {0} {1}".format(self.param1,self.param2))

    @classmethod
    def tearDownClass(cls):
        pass #print("\ntearDownClass: tear down class")


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    for p1, p2 in [(1, 2), (3, 4)]:
        suite.addTest(GeneralTestCase('runTest', p1, p2))
    
    return suite

import argparse
import sys
def main(argv=None):
    global settings
     
    # usage: python tests/test_dynamic_unittest.py
    parser = argparse.ArgumentParser(description="Do something.")
    parser.add_argument('--collection', type=str, required=True)
    parser.add_argument('--version', type=float, required=True)
    parser.add_argument('--git-commit', type=str, required=True)
    parser.add_argument('--print-style', type=str, required=True)

    args = parser.parse_args(argv)
    
    settings = vars(args) 

    command = "unittest -v"

    unittest.main(argv=command.split(" "))

if __name__ == '__main__':
    main()
