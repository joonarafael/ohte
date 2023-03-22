import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)
    
    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1000.00 euroa, lounaita myyty 0 kappaletta.")
    
    #KATEINEN
    def test_syo_edullisesti_kun_rahat_riittavat(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1002.40 euroa, lounaita myyty 1 kappaletta.")

    def test_syo_maukkaasti_kun_rahat_riittavat(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1004.00 euroa, lounaita myyty 1 kappaletta.")

    def test_syo_edullisesti_kun_rahat_eivat_riita(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1000.00 euroa, lounaita myyty 0 kappaletta.")

    def test_syo_maukkaasti_kun_rahat_eivat_riita(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1000.00 euroa, lounaita myyty 0 kappaletta.")
    
    #KORTTI
    def test_syo_edullisesti_kun_kortti_riittaa(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1000.00 euroa, lounaita myyty 1 kappaletta.")
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 7.60 euroa")

    def test_syo_maukkaasti_kun_kortti_riittaa(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1000.00 euroa, lounaita myyty 1 kappaletta.")
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 6.00 euroa")
    
    def test_syo_edullisesti_kun_kortti_ei_riita(self):
        uusi_kortti = Maksukortti(200)

        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(uusi_kortti), False)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1000.00 euroa, lounaita myyty 0 kappaletta.")
        self.assertEqual(str(uusi_kortti), "Kortilla on rahaa 2.00 euroa")

    def test_syo_maukkaasti_kun_kortti_ei_riita(self):
        uusi_kortti = Maksukortti(360)

        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(uusi_kortti), False)
        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1000.00 euroa, lounaita myyty 0 kappaletta.")
        self.assertEqual(str(uusi_kortti), "Kortilla on rahaa 3.60 euroa")
    
    def test_kortin_saldon_lataus_onnistuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 2000)

        self.assertEqual(str(self.kassapaate), "Kassassa on rahaa 1020.00 euroa, lounaita myyty 0 kappaletta.")
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 30.00 euroa")