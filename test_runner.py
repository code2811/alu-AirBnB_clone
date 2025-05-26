#!/usr/bin/python3
"""Simple test runner that works with Python 3.4."""

import unittest
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests():
    """Discover and run all tests."""
     
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print("Tests run: {}".format(result.testsRun))
    print("Failures: {}".format(len(result.failures)))
    print("Errors: {}".format(len(result.errors)))
    
    if result.wasSuccessful():
        print("STATUS: ✅ ALL TESTS PASSED")
        return 0
    else:
        print("STATUS: ❌ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
