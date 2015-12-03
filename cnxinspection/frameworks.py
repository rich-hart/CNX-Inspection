import unittest
import psycopg2
import cv2
import cv
import numpy

START_TEST = END_TEST = "*"*70   

################################################################
# FIXME: This class should be able to be run with the default  # 
# unittests conventions, e.g. the default load_tests function. #
################################################################
class PNGs(unittest.TestCase):
    def __init__(self, methodName, page1=None, page2=None):
        new_test_name = "({0},{1},{2})".format(methodName,page1,page2)
        test = getattr(self,methodName)
        setattr(PNGs, new_test_name,test)
        super(PNGs, self).__init__(new_test_name)
        self.page1 = page1
        self.page2 = page2
        self.metric = methodName

    @classmethod
    def setUpClass(cls):
        cls._con = psycopg2.connect(database="training-data",user="qa")

        cls._text_runner.stream.writeln(START_TEST)

    def setUp(self):

        self.cur = self._con.cursor()

        self.cur.execute("SELECT png FROM pngs_a WHERE page_number=(%s)",(self.page1,))

        data = self.cur.fetchone()[0]

        self.img_i=cv2.imdecode(numpy.asarray(data),flags=cv2.CV_LOAD_IMAGE_COLOR)

        self.cur.execute("SELECT png FROM pngs_b WHERE page_number=(%s)",(self.page2,))
 
        data = self.cur.fetchone()[0]

        self.img_j=cv2.imdecode(numpy.asarray(data),flags=cv2.CV_LOAD_IMAGE_COLOR)

        # Save current attributes
        self.setUp_attrList = None
        self.setUp_attrList = dir(self)



    def tearDown(self):
#        if sys.exc_info() == (None,None,None):
#            pass # test ok
#        else:
#            pass # test failed
        new_attrList = list(set(dir(self)) - set(self.setUp_attrList))
        if new_attrList:
            strList = ["({0},{1})".format(attr,getattr(self,attr)) for attr in new_attrList ]
            variable_str = " ".join(strList)
            self._text_runner.stream.writeln(variable_str)

    @classmethod
    def tearDownClass(cls):
        cls._text_runner.stream.writeln(END_TEST)



