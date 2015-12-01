import unittest
import psycopg2

settings = None

class GeneralTestCase(unittest.TestCase):
    def __init__(self, methodName, param1=None, param2=None):
        test_name = "{0}: params=({1},{2})".format(methodName,param1,param2)
        test = getattr(self,methodName)
        setattr(GeneralTestCase, test_name,test)
        super(GeneralTestCase, self).__init__(test_name)
        self.param1 = param1
        self.param2 = param2


class TestPNGs(GeneralTestCase):

    @classmethod
    def setUpClass(cls):
        cls._con = psycopg2.connect(database=settings['database'],user=settings['user'])
        cls._settings = settings         

    def setUp(self):
        self.cur = self._con.cursor()
        self.cur.execute("SELECT png FROM pngs_a WHERE page_number=1")
        self.png_i = self.cur.fetchone()[0]
        self.cur.execute("SELECT png FROM pngs_b WHERE page_number=1")
        self.png_j = self.cur.fetchone()[0]      
#        pass #print("\nsetUp: setup up {0} {1}".format(self.param1,self.param2))

    def test_pages_equal(self):
#        import ipdb;ipdb.set_trace();
        pass #print("\nrunTest: testing {0} {1}".format(self.param1,self.param2)) # Test that depends on param 1 and 2.

    def test_second_test_type(self):
        pass

    def tearDown(self):
        pass #print("\ntearDown: tear down {0} {1}".format(self.param1,self.param2))

    @classmethod
    def tearDownClass(cls):
        pass #print("\ntearDownClass: tear down class")


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    con = psycopg2.connect(database=settings['database'],user=settings['user'])
    cur = con.cursor()
    cur.execute('SELECT COUNT(page_number) FROM pngs_a')
    total_pgns_a=cur.fetchone()[0]
    cur.execute('SELECT COUNT(page_number) FROM pngs_b')
    total_pgns_b=cur.fetchone()[0]
    test_params =[ (i,j) for i in range(1,total_pgns_a+1) for j in range(1,total_pgns_b+1)] 
    for p1, p2 in test_params:
#        suite.addTest(GeneralTestCase('runTest',p1,p2))
        suite.addTest(TestPNGs('test_pages_equal', p1, p2))
#        suite.addTest(TestPNGs('test_second_test_type', p1, p2)) 
    return suite

import argparse
import sys
def main(argv=None):
    global settings
     
    # usage: python dynamic_unittest.py --collection col1 --version 1.1 --git-commit asfd --print-style asd
    parser = argparse.ArgumentParser(description="**add discription**")

    parser.add_argument('--collection', type=str, required=True)
    parser.add_argument('--version', type=float, required=True)
    parser.add_argument('--git-commit', type=str, required=True)
    parser.add_argument('--print-style', type=str, required=True)
    parser.add_argument('--database', type=str, default = "training-data")
    parser.add_argument('--user', type=str, default = "qa")

    args = parser.parse_args(argv)
    
    settings = vars(args) 

    command = "unittest -v"

    unittest.main(argv=command.split(" "))

if __name__ == '__main__':
    main()
