
import bottle
import unittest
from boddle import boddle
from app import simpandata

# localhost:3000/simpandata?tds=1000&suhu=35&ph=9

# Test case 1


class AppTesting(unittest.TestCase):
    def testNonDigitQuery(self):
        with boddle(path='api/simpandata', method='get', query={'tinggi': 'a', 'ec': 'b', 'ph': 'c'}):
            self.assertEqual(
                simpandata(), 'Data masukan tidak memenuhi format masukan')

# Test case 2

    def testTrueQuery(self):

        with boddle(path='api/simpandata', method='get', query={'tinggi': '35', 'ec': '1000', 'ph': '9'}):
            self.assertEqual(
                simpandata(), "The value of tinggi is: 35 and the value of EC is: 1000 and the value of ph is: 9")


# Test case 3

    def testMissingQuery(self):

        with boddle(path='api/simpandata', method='get', query={'tinggi': '35', 'ec': '1000'}):
            self.assertEqual(
                simpandata(), "Data masukan tidak memenuhi format masukan")


if __name__ == '__main__':
    unittest.main()
