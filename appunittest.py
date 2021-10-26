import bottle
import unittest
from boddle import boddle
from app import simpandata


class AppTesting(unittest.TestCase):

# Test case 1-2-3-4-5-6-11

    def testTrueQuery(self):
        n_tinggi = 35.3
        n_ec = 960.8
        n_ph = 7.2
        with boddle(path='api/simpandata', method='get', query={'tinggi': n_tinggi, 'ec': n_ec, 'ph': n_ph}):
            self.assertEqual(
                simpandata(), "Nilai tinggi: "+str(n_tinggi)+", Nilai EC: "+str(n_ec)+", dan Nilai PH: "+str(n_ph))

# Test case 1-2-10-11

    def testMissingTinggi(self):
        n_ec = 960.8
        n_ph = 7.2
        with boddle(path='api/simpandata', method='get', query={'ec': n_ec, 'ph': n_ph}):
            self.assertEqual(
                simpandata(), "Data masukan Tinggi Nutrisi tidak ditemukan")

# Test case 1-2-3-9-11

    def testMissingEC(self):
        n_tinggi = 35.3
        n_ph = 7.2
        with boddle(path='api/simpandata', method='get', query={'tinggi': n_tinggi, 'ph': n_ph}):
            self.assertEqual(
                simpandata(), "Data masukan EC tidak ditemukan")


# Test case 1-2-3-4-8-11


    def testMissingPH(self):
        n_tinggi = 35.3
        n_ec = 960.8
        with boddle(path='api/simpandata', method='get', query={'tinggi': n_tinggi, 'ec': n_ec}):
            self.assertEqual(
                simpandata(), "Data masukan PH tidak ditemukan")

# Test case 1-2-3-4-8-11

    def testNonDigitQuery(self):
        with boddle(path='api/simpandata', method='get', query={'tinggi': 'a', 'ec': 'b', 'ph': 'c'}):
            self.assertEqual(
                simpandata(), 'Data masukan tidak dalam bentuk digit')

# Test case dummy

    def testNonDigitQuerya(self):
        with boddle(path='api/simpandata', method='get', query={'tinggi': 'a', 'ec': 'b', 'ph': 'c'}):
            self.assertEqual(
                simpandata(), 'Data masukan tidak dalam bentuk digit')

# Test case dummy

    def testNonDigitQueryb(self):
        with boddle(path='api/simpandata', method='get', query={'tinggi': 'a', 'ec': 'b', 'ph': 'c'}):
            self.assertEqual(
                simpandata(), 'Data masukan tidak dalam bentuk digit')

# Test case dummy

    def testNonDigitQueryc(self):
        with boddle(path='api/simpandata', method='get', query={'tinggi': 'a', 'ec': 'b', 'ph': 'c'}):
            self.assertEqual(
                simpandata(), 'Data masukan tidak dalam bentuk digit')

# Test case dummy

    def testNonDigitQueryd(self):
        with boddle(path='api/simpandata', method='get', query={'tinggi': 'a', 'ec': 'b', 'ph': 'c'}):
            self.assertEqual(
                simpandata(), 'Data masukan tidak dalam bentuk digit')

# Test case dummy

    def testNonDigitQuerye(self):
        with boddle(path='api/simpandata', method='get', query={'tinggi': 'a', 'ec': 'b', 'ph': 'c'}):
            self.assertEqual(
                simpandata(), 'Data masukan tidak dalam bentuk digit')

if __name__ == '__main__':
    unittest.main()
