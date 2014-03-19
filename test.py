import unittest
import kapall

class test(unittest.TestCase):

    def test_Spil(self):
        tilraunadyr = kapall.Spil('Hjarta',1,True)
        self.assertEqual(tilraunadyr.hvernig_snyrdu(),True)
        tilraunadyr.snua()
        self.assertEqual(tilraunadyr.hvernig_snyrdu(),False)
        self.assertEqual(tilraunadyr.fa_spil(), (192, -1))
        self.assertEqual(tilraunadyr.haed(), 96)
        self.assertEqual(tilraunadyr.breidd(), 72)

    def test_bunka(self):
        tilraunadyr = kapall.Bunki(200,200)
        self.assertEqual(tilraunadyr.tomur(),True)
        tilraunadyr.setja_draug()
        self.assertEqual(tilraunadyr.draugur_lifandi(),True)
        spil = []
        for i in range(5):
            spil.append(kapall.Spil('Hjarta',i+1, True))
        tilraunadyr.taka_draug()
        tilraunadyr.setja_a(spil)
        self.assertEqual(tilraunadyr.tomur(),False)
        self.assertEqual(tilraunadyr.draugur_lifandi(),False)
        self.assertEqual(tilraunadyr.taka_af(spil[0]),spil)
        self.assertEqual(tilraunadyr.tomur(),True)

    def test_stokk(self):
        tilraunadyr = kapall.Stokkur(200,200)
        self.assertEqual(tilraunadyr.tomur(),True)
        tilraunadyr.setja_draug()
        self.assertEqual(tilraunadyr.draugur_lifandi(),True)
        spil = []
        for i in range(5):
            spil.append(kapall.Spil('Hjarta',i+1, True))
        tilraunadyr.taka_draug()
        tilraunadyr.setja_a(spil)
        self.assertEqual(tilraunadyr.tomur(),False)
        self.assertEqual(tilraunadyr.draugur_lifandi(),False)
        self.assertEqual(tilraunadyr.taka_af(spil[0]),[spil[-1]])
        self.assertEqual(tilraunadyr.tomur(),False)


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)