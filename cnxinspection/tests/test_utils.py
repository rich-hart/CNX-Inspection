import unittest
import os

from ..utils import *

LOG_FILE_PATH = "cnxinspection/tests/data/log_file.txt"

class TestUtils(unittest.TestCase):
     def test_log_parser(self):
         with open(os.path.abspath(LOG_FILE_PATH)) as f:
              f.read()
