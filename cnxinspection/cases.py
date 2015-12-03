import unittest
import psycopg2
import cv2
import cv
import numpy

from frameworks import PNGs

class DefaultTest(PNGs):

    def imgs_equal(self):
        self.assertTrue(numpy.array_equal(self.img_i,self.img_j))

    def hist_corr_greater_threshhold(self):
        threshold=.96
        hist_i = cv2.calcHist([self.img_i],[0],None,[256],[0,256])
        hist_j = cv2.calcHist([self.img_j],[0],None,[256],[0,256])       
        measure = cv2.compareHist(hist_i,hist_j,method=cv.CV_COMP_CORREL)
        self.assertGreater(measure,threshold)

class MyTest(PNGs):

    def random_test(self):
        if self.page1 != 2 and self.page2 !=3:
            raise unittest.SkipTest("**reason skipped**")

    # FIXME: new params can be saved in log file by giving self
    # a new attribute .e.g. self.threshold = .6.  This messes
    # up log file parsing
    def hist_bhatta_greater_threshhold(self):
        threshold=0.2
        hist_i = cv2.calcHist([self.img_i],[0],None,[256],[0,256])
        hist_j = cv2.calcHist([self.img_j],[0],None,[256],[0,256])       
        measure = cv2.compareHist(hist_i,hist_j,method=cv.CV_COMP_BHATTACHARYYA)
        self.assertLess(measure,threshold)

