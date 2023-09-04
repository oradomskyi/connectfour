import unittest

print(__package__, __name__)
from Game.test.TestGame import TestGame


def suite():
    print(__package__, __name__)
    suite = unittest.TestSuite()
    suite.addTest(TestGame('test_ctor_correct_args'))
    # suite.addTest(TestGame('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())