import unittest
import Invoicer # this also imports all sub-modules

class InvoicerTests(unittest.TestCase):
    def test_five(self):
        assert 5+5 == 10


if __name__ == '__main__':
    unittest.main()

