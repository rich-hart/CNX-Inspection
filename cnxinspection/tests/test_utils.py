import unittest
import os

from ..utils import *

LOG_FILE_PATH = "cnxinspection/tests/data/log_file.txt"

class TestUtils(unittest.TestCase):
     def test_log_parser(self):
         matrix = log_parser(os.path.abspath(LOG_FILE_PATH))
         dimensions = matrix.shape
     
         for page_x in range(0,dimensions[0]):
             for page_y in range(0,dimensions[1]):
                 for method_index in range(0,dimensions[2]):
                     if page_x == 0 or page_y == 0:
                         returned_value = matrix[page_x][page_y][method_index]
                         self.assertEqual(returned_value,0)
     def test_matrix_equality(self):
         matrix = log_parser(os.path.abspath(LOG_FILE_PATH))
         (d1,d2,total_methods) = matrix.shape
         return_matrix = matrix_equality(matrix,['or']*(total_methods-1))
     def test_LCSLength(self):
         matrix = log_parser(os.path.abspath(LOG_FILE_PATH))
         (d1,d2,total_methods) = matrix.shape
         new_matrix = matrix_equality(matrix,['or']*(total_methods-1))
         return_matrix = LCSLength(new_matrix )

     def test_backtrack(self):
         matrix = log_parser(os.path.abspath(LOG_FILE_PATH))
         (d1,d2,total_methods) = matrix.shape
         R = matrix_equality(matrix,['or']*(total_methods-1))
         C = LCSLength(R)
         LCS = backtrack(C,R)
