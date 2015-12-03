import sys
import argparse

from cases import *
from frameworks import PNGs
# from frameworks import load_png_tests as load_tests

settings = None
test_runner = None

##################################################################
# FIXME: The load_tests function should be moved to the          # 
# 'frameworks' module under the name load_png_tests.  Then the   #
# function should be imported into this module with the command  #
# 'from frameworks import load_png_tests as load_tests'.         #
##################################################################
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    con = psycopg2.connect(database="training-data",user="qa")
    cur = con.cursor()
    cur.execute('SELECT COUNT(page_number) FROM pngs_a')
    total_pgns_a=cur.fetchone()[0]
    cur.execute('SELECT COUNT(page_number) FROM pngs_b')
    total_pgns_b=cur.fetchone()[0]
    test_params =[ (i,j) for i in range(1,total_pgns_a+1) for j in range(1,total_pgns_b+1)]
    all_metrics = []
    test_cases =  [ eval(case) for case in settings['include']]
    for case in test_cases:
        setattr(case,"_text_runner",text_runner)
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

    return suite

def main(argv=None):
    global settings
    global text_runner

    parser = argparse.ArgumentParser()

    parser.add_argument('--include', action='append', default = ["DefaultTest"])
    parser.add_argument('--exclude', action='append', default = [])

    args = parser.parse_args(argv)
    
    args.include = list(set(args.include)-set(args.exclude))

    settings = vars(args) 

    command = "unittest".split(" ")
    
    log_file = 'log_file.txt'
    with open(log_file, "w") as f:  
        f = open(log_file, "w")
        text_runner = unittest.TextTestRunner(f,verbosity=2)
        unittest.main(argv=command,testRunner=text_runner)

if __name__ == '__main__':
    main()
