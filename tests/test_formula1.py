import math
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from formula1 import (Parametres, circuit_convenable, circuit_en_svg,
                      contient_demi_tour, depuis_geometrie, est_ferme, longueur,
                      representation_minimale, temps_course, temps_droite,
                      temps_tour, vitesse_recommandee, vitesses_entree_max)
from formula1.cli import main

P = Parametres()


class Geometrie(unittest.TestCase):
    def test_longueur(self):
        self.assertEqual(longueur(list("AGAGAADAGA"), 100), 600)

    def test_representation_minimale(self):
        c = ["A", "A", "G", "D", "G", "G", "G", "A"]
        self.assertEqual(representation_minimale(c), ["A", "A", "D", "A"])
        self.assertEqual(representation_minimale(list("GGGG")), [])

    def test_ferme(self):
        self.assertTrue(est_ferme(list("ADADADAD")))
        self.assertFalse(est_ferme(list("AADAADAADAAD")[:-1]))
        self.assertFalse(est_ferme(list("AAAA")))

    def test_demi_tour(self):
        self.assertTrue(contient_demi_tour(list("AGGA")))
        self.assertTrue(contient_demi_tour(list("ADDA")))
        self.assertTrue(contient_demi_tour(list("AGDGGA")))  # GD annulés, reste GG
        self.assertFalse(contient_demi_tour(list("AGADAGA")))
        # demi-tour à cheval sur la fin et le début de la liste
        self.assertTrue(contient_demi_tour(list("GAAAG")))

    def test_convenable(self):
        self.assertTrue(circuit_convenable(list("ADADADAD")))
        self.assertTrue(circuit_convenable(list("AAADADAAGADADAAD")))
        # fermé, sans demi-tour, mais le tracé repasse par un même point
        self.assertFalse(circuit_convenable(list("AAGAGAGAADADAD")))
        # non fermé
        self.assertFalse(circuit_convenable(list("AADAAD")))
        self.assertFalse(circuit_convenable([]))

    def test_croisement_detecte(self):
        c = list("AAGAGAGAADADAD")
        self.assertTrue(est_ferme(c) and not contient_demi_tour(c))
        self.assertFalse(circuit_convenable(c))

    def test_invalide(self):
        with self.assertRaises(ValueError):
            est_ferme(list("AXA"))

    def test_conversion(self):
        self.assertEqual(depuis_geometrie(list("AADA"), 10, 5),
                         [("D", 20), ("V", 5), ("D", 10)])


class Cinematique(unittest.TestCase):
    def test_droite_cas_palier(self):
        # 0 -> 100 en 10 s (500 m), 100 -> 0 en 5 s (250 m), palier de 250 m
        self.assertAlmostEqual(temps_droite(1000, 0, 0), 10 + 5 + 250 / 100)

    def test_droite_pointe_intermediaire(self):
        d = 300
        t = temps_droite(d, 0, 0)
        v3 = math.sqrt(2 * 10 * 20 * d / 30)
        self.assertAlmostEqual(t, v3 / 10 + v3 / 20)

    def test_droite_impossible(self):
        with self.assertRaises(ValueError):
            temps_droite(10, 0, 50)  # il faut 125 m
        with self.assertRaises(ValueError):
            temps_droite(10, 50, 0)  # il faut 62.5 m

    def test_droite_limite_exacte(self):
        self.assertAlmostEqual(temps_droite(125, 0, 50), 5.0)

    def test_droite_simulation(self):
        """Compare à une simulation par pas de temps (bang-bang) pour d < dmin."""
        d, v1, v2 = 400.0, 20.0, 30.0
        v3 = math.sqrt((2 * 10 * 20 * d + 20 * v1**2 + 10 * v2**2) / 30)
        dt, t, x, v = 1e-5, 0.0, 0.0, v1
        while v < v3:
            v += 10 * dt; x += v * dt; t += dt
        while v > v2:
            v -= 20 * dt; x += v * dt; t += dt
        self.assertAlmostEqual(x, d, delta=0.5)
        self.assertAlmostEqual(temps_droite(d, v1, v2), t, delta=1e-2)

    def test_vitesses_entree(self):
        c = [("V", 50), ("D", 100), ("V", 30), ("D", 200)]
        b = vitesses_entree_max(c, 50)
        self.assertAlmostEqual(b[3], min(P.vmax, math.sqrt(50**2 + 2 * 20 * 200)))
        self.assertAlmostEqual(b[2], min(vitesse_recommandee(30), b[3]))
        self.assertAlmostEqual(b[1], min(P.vmax, math.sqrt(b[2]**2 + 2 * 20 * 100)))
        for v in b:
            self.assertLessEqual(v, P.vmax)

    def test_tour_monotone_et_coherent(self):
        c = [("D", 300), ("V", 50), ("D", 200), ("V", 30)]
        lent = temps_tour(c, 0, 20)
        rapide = temps_tour(c, 0, 100)
        self.assertGreaterEqual(lent, rapide - 1e-9)
        # partir plus vite ne peut pas faire perdre de temps
        self.assertLessEqual(temps_tour(c, 20, 100), rapide)

    def test_tour_v0_trop_elevee(self):
        with self.assertRaises(ValueError):
            temps_tour([("V", 4), ("D", 10)], 100, 100)

    def test_course(self):
        c = depuis_geometrie(list("ADADADAD"), 200, 30)
        t1 = temps_course(c, 1)
        t5 = temps_course(c, 5)
        t6 = temps_course(c, 6)
        self.assertGreater(t5, t1)
        # ajouter un tour en régime établi coûte le même temps
        t7 = temps_course(c, 7)
        self.assertAlmostEqual(t7 - t6, t6 - t5, places=6)
        self.assertLess(t6 - t5, t1)  # un tour lancé est plus rapide qu'un départ arrêté
        with self.assertRaises(ValueError):
            temps_course(c, 0)

    def test_course_arc(self):
        c = depuis_geometrie(list("ADADADAD"), 200, 30)
        self.assertGreater(temps_course(c, 3, arc_virage=True), temps_course(c, 3))


class Divers(unittest.TestCase):
    def test_svg(self):
        svg = circuit_en_svg(list("ADADADAD"))
        self.assertTrue(svg.startswith("<svg") and svg.endswith("</svg>"))

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "c.svg")
            self.assertEqual(main(["--exemple", "en_L", "--svg", f]), 0)
            self.assertTrue(os.path.exists(f))
        self.assertEqual(main(["AXA"]), 2)
        self.assertEqual(main(["AAA"]), 0)


if __name__ == "__main__":
    unittest.main()
