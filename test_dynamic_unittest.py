#http://stackoverflow.com/questions/32899/how-to-generate-dynamic-parametrized-unit-tests-in-python
import unittest

l = [["page_1", "a", "a",], ["page_2", "a", "b"], ["page_3", "b", "b"]]

class TestSequense(unittest.TestCase):
    pass

def test_generator(a, b):
    def test(self):
        self.assertEqual(a,b)
    return test

if __name__ == '__main__':
    for t in l:
        test_name = 'test_%s' % t[0]
        test = test_generator(t[1], t[2])
        setattr(TestSequense, test_name, test)
    unittest.main()

