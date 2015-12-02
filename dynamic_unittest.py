import unittest
import psycopg2
import cv2
import cv
import numpy

import sys
import argparse
import logging

settings = None
#logger = None
test_runner = None
results = {}

results = None

START_TEST = END_TEST = "*"*70
# Notes: use db scoring table for training current svgs
# save the log file for long term storage for each test
# Be able to parse the log file back into db scoring tabl
class PNGs(unittest.TestCase):
    def __init__(self, methodName, param1=None, param2=None):
        new_test_name = "{0}({1},{2})".format(methodName,param1,param2)
        test = getattr(self,methodName)
        setattr(PNGs, new_test_name,test)
        super(PNGs, self).__init__(new_test_name)
        self.param1 = param1
        self.param2 = param2
        self.metric = methodName

    @classmethod
    def setUpClass(cls):
        cls._con = psycopg2.connect(database=settings['database'],user=settings['user'])

        cls._settings = settings

        text_runner.stream.writeln(START_TEST)
        
        cls._text_runner=text_runner       

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


    def tearDown(self):
        if sys.exc_info() == (None,None,None):
            pass # test ok
        else:
            pass # test failed

        new_attrList = list(set(dir(self)) - set(self.setUp_attrList))
        if new_attrList:
            strList = ["{0} = {1}".format(attr,getattr(self,attr)) for attr in new_attrList ]
            variable_str = ", ".join(strList)
            text_runner.stream.writeln(variable_str)

    @classmethod
    def tearDownClass(cls):
        cls._text_runner.stream.writeln(END_TEST)

class MyTest_1(PNGs):

    def imgs_equal(self):
        self.assertTrue(numpy.array_equal(self.img_i,self.img_j))

    def hist_corr_greater_threshhold(self):
        self.threshold=.96
        hist_i = cv2.calcHist([self.img_i],[0],None,[256],[0,256])
        hist_j = cv2.calcHist([self.img_j],[0],None,[256],[0,256])       
        measure = cv2.compareHist(hist_i,hist_j,method=cv.CV_COMP_CORREL)
        self.assertGreater(measure,self.threshold)

class MyTest_2(PNGs):

    def hist_bhatta_greater_threshhold(self):
        self.threshold=0.2
        hist_i = cv2.calcHist([self.img_i],[0],None,[256],[0,256])
        hist_j = cv2.calcHist([self.img_j],[0],None,[256],[0,256])       
        measure = cv2.compareHist(hist_i,hist_j,method=cv.CV_COMP_BHATTACHARYYA)
        self.assertLess(measure,self.threshold)


test_cases = (MyTest_1,MyTest_2)

def load_tests(loader, tests, pattern):
    global results
    suite = unittest.TestSuite()
    con = psycopg2.connect(database=settings['database'],user=settings['user'])
    cur = con.cursor()
    cur.execute('SELECT COUNT(page_number) FROM pngs_a')
    total_pgns_a=cur.fetchone()[0]
    cur.execute('SELECT COUNT(page_number) FROM pngs_b')
    total_pgns_b=cur.fetchone()[0]
    test_params =[ (i,j) for i in range(1,total_pgns_a+1) for j in range(1,total_pgns_b+1)]
    all_metrics = []


    for case in test_cases:
        test_pngs_methods=[method for method in dir(case) if callable(getattr(case, method))]
        unittests_methods=[method for method in dir(PNGs) if callable(getattr(PNGs, method))]
        test_metrics = list(set(test_pngs_methods) - set(unittests_methods))
        if set(test_metrics).intersection(set(all_metrics)) == set([]):
            all_metrics=all_metrics+test_metrics
        else:
            raise NameError("method names must be unique for all test cases.")
        for metric in test_metrics:
            for i, j in test_params:
                suite.addTest(case(metric, i, j))
#    suite.run(results)
    return suite


def main(argv=None):
    global settings
    global results
    global text_runner

#    logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
#    logger = logging.getLogger('Tests')
#    logger.setLevel(logging.ERROR)
#    sys.stderr.write("test")
    #create console handler with a higher log level
#    ch = logging.StreamHandler(sys.stderr)
#    ch.setLevel(logging.ERROR) 
#    logger.addHandler(ch)
#    logger.addHandler(logging.StreamHandler(sys.stderr))
#    sys.stderr.write("hello")
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

    command = "unittest"
#    results = unittest.TextTestRunner(verbosity=2)
    log_file = 'log_file.txt'
    with open(log_file, "w") as f:  
        f = open(log_file, "w")
        text_runner = unittest.TextTestRunner(f,verbosity=2)
        unittest.main(argv=command.split(" "),testRunner=text_runner)


if __name__ == '__main__':
    main()
