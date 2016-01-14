from unittest import TestCase
from astropandas import Table

class TestTable(TestCase):
    def setUp(self):
        self.t = Table.read('tests/merged.fits')
        self.df = self.t.to_pandas()

    def test_to_pandas(self):
        for i in range(3):
            self.assertIn('SPECTRO_MAG({})'.format(i), self.df.columns)
