import unittest
import psycopg2
import cv2
import cv
import numpy

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

        self.cur.execute("SELECT png FROM pngs_a WHERE page_number=(%s)",(self.param1,))
        try:
            data = self.cur.fetchone()[0]
        except(TypeError):
            raise unittest.SkipTest("png_a[{0}] is None".format(self.param1))
        self.img_i=cv2.imdecode(numpy.asarray(data),flags=cv2.CV_LOAD_IMAGE_COLOR)


        self.cur.execute("SELECT png FROM pngs_b WHERE page_number=(%s)",(self.param1,))
        try: 
            data = self.cur.fetchone()[0]
        except(TypeError):
            raise unittest.SkipTest("png_b[{0}] is None".format(self.param2))
        self.img_j=cv2.imdecode(numpy.asarray(data),flags=cv2.CV_LOAD_IMAGE_COLOR)



    def test_imgs_equal(self):
        self.assertTrue(numpy.array_equal(self.img_i,self.img_j))

    def test_hist_equal(self):
        self.hist_i = cv2.calcHist([self.img_i],[0],None,[256],[0,256])
        self.hist_j = cv2.calcHist([self.img_j],[0],None,[256],[0,256])       
        comp_value = cv2.compareHist(self.hist_i,self.hist_j,method=cv.CV_COMP_CORREL)
        self.assertEqual(comp_value,1.0)

    def tearDown(self):
#        print("tear down ran")
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
    for i, j in test_params:
#        suite.addTest(GeneralTestCase('runTest',p1,p2))
        suite.addTest(TestPNGs('test_imgs_equal', i, j))
        suite.addTest(TestPNGs('test_hist_equal', i, j))
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
