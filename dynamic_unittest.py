
# More examples:
# http://stackoverflow.com/questions/32899/how-to-generate-dynamic-parametrized-unit-tests-in-python
# USE THIS ONE!!!!! --- > https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests

#import unittest


#class NumbersTest(unittest.TestCase):

#    def test_even(self):
#        """
#        Test that numbers between 0 and 5 are all even.
#        """
#        for i in range(0, 6):
#            with self.subTest(i=i):
#                self.assertEqual(i % 2, 0)


#import unittest

#l = [["page_1", "a", "a",], ["page_2", "a", "b"], ["page_3", "b", "b"]]

#class TestSequense(unittest.TestCase):
#    pass

#def test_generator(a, b):
#    def test(self):
#        self.assertEqual(a,b)
#    return test

#if __name__ == '__main__':
#    for t in l:
#        test_name = 'test_%s' % t[0]
#        test = test_generator(t[1], t[2])
#        setattr(TestSequense, test_name, test)
#    unittest.main()

import unittest

settings = None

class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

class GeneralTestCase(unittest.TestCase):
    def __init__(self, methodName, param1=None, param2=None):
        super(GeneralTestCase, self).__init__(methodName)

        self.param1 = param1
        self.param2 = param2

    @classmethod
    def setUpClass(cls):
        global settings
        print("\nsetUpClass: setup up class")
        cls.settings = settings
        print(cls.settings)


    def setUp(self):
        print("\nsetUp: setup up {0} {1}".format(self.param1,self.param2))

    def runTest(self):
        print("\nrunTest: testing {0} {1}".format(self.param1,self.param2)) # Test that depends on param 1 and 2.

    def tearDown(self):
        print("\ntearDown: tear down {0} {1}".format(self.param1,self.param2))

    @classmethod
    def tearDownClass(cls):
        print("\ntearDownClass: tear down class")

test_cases = (TestStringMethods, )

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

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


