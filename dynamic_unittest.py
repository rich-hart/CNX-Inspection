import unittest
import psycopg2
import cv2
import cv
import numpy

from sys import exc_info

settings = None

# Notes: use db scoring table for training current svgs
# save the log file for long term storage for each test
# Be able to parse the log file back into db scoring tabl

class GeneralTestCase(unittest.TestCase):
    def __init__(self, methodName, param1=None, param2=None):
        new_test_name = "{0}({1},{2})".format(methodName,param1,param2)
        test = getattr(self,methodName)
        setattr(GeneralTestCase, new_test_name,test)
        super(GeneralTestCase, self).__init__(new_test_name)
        self.param1 = param1
        self.param2 = param2
        self.metric = methodName

#    def runTest(self):
#        pass

class TestPNGs(GeneralTestCase):

    @classmethod
    def setUpClass(cls):
        cls._con = psycopg2.connect(database=settings['database'],user=settings['user'])
        cls._settings = settings         

    def setUp(self):
        self.cur = self._con.cursor()

        self.cur.execute("SELECT png FROM pngs_a WHERE page_number=(%s)",(self.param1,))

        data = self.cur.fetchone()[0]

        self.img_i=cv2.imdecode(numpy.asarray(data),flags=cv2.CV_LOAD_IMAGE_COLOR)

        self.cur.execute("SELECT png FROM pngs_b WHERE page_number=(%s)",(self.param2,))
 
        data = self.cur.fetchone()[0]

        self.img_j=cv2.imdecode(numpy.asarray(data),flags=cv2.CV_LOAD_IMAGE_COLOR)

        # Save current attributes
        self.setUp_attrList = None

        self.setUp_attrList = dir(self)

    def imgs_equal(self):
        self.assertTrue(numpy.array_equal(self.img_i,self.img_j))

    def hist_comp_greater_threshhold(self):
        self.threshold=.96
        hist_i = cv2.calcHist([self.img_i],[0],None,[256],[0,256])
        hist_j = cv2.calcHist([self.img_j],[0],None,[256],[0,256])       
        metric = cv2.compareHist(hist_i,hist_j,method=cv.CV_COMP_CORREL)
        self.assertGreater(metric,self.threshold)

    def tearDown(self):
#        if exc_info() == (None,None,None):
#            test passed
#        else:
#            test failed

        new_attrList = list(set(dir(self)) - set(self.setUp_attrList))
        strList = ["{0} = {1}".format(attr,getattr(self,attr)) for attr in new_attrList ]
        variable_str = ", ".join(strList)
        print(variable_str + " ...")

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
    test_pngs_methods=[method for method in dir(TestPNGs) if callable(getattr(TestPNGs, method))]
    unittests_methods=[method for method in dir(unittest.TestCase) if callable(getattr(unittest.TestCase, method))]
    test_metrics = list(set(test_pngs_methods) - set(unittests_methods))
    for metric in test_metrics:
        for i, j in test_params:
    #        suite.addTest(GeneralTestCase('runTest', i ,j ))
            suite.addTest(TestPNGs(metric, i, j))
#            suite.addTest(TestPNGs(metric, i, j))
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
    parser.add_argument('--exclude-tests', type=str)

    args = parser.parse_args(argv)
    
    settings = vars(args)

    settings['metrics'] = None 

    command = "unittest -v"

    unittest.main(argv=command.split(" "))

if __name__ == '__main__':
    main()
