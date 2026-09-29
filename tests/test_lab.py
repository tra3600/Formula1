import contextlib
import io
import math
import os
import random
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from formula1 import (Parametres, circuit_convenable, depuis_geometrie, longueur,
                      temps_course, temps_droite, temps_tour)
from formula1 import analyses as an
from formula1 import profil as pf
from formula1.cas import CAS, EXEMPLES, FORMES, Sortie, lancer
from formula1.cinematique import vitesse_de_ligne, vitesse_recommandee
from formula1.cli import main
from formula1.dessin import circuit_vitesse_svg, graphe_svg
from formula1.enumeration import (circuit_depuis_cases, circuits, nombre_polygones_fixes)
from formula1.geometrie import carte_segments, diagnostic, est_ferme, rotations

P = Parametres()


def silencieux(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        r = f(*a, **k)
    return r, buf.getvalue()


class Diagnostic(unittest.TestCase):
    def test_equivaut_a_convenable(self):
        random.seed(3)
        for _ in range(5000):
            w = [random.choice("AAAGD") for _ in range(random.randint(0, 14))]
            self.assertEqual(diagnostic(w) == [], circuit_convenable(w), "".join(w))

    def test_raisons(self):
        self.assertIn("non fermé", diagnostic(list("AAGAAGA"))[0])
        self.assertIn("cap final", diagnostic(list("AGAGAGA"))[0])
        self.assertTrue(any("demi-tour" in r for r in diagnostic(list("AGGA"))))
        self.assertTrue(any("croisement" in r for r in diagnostic(list("AAGAGAGAADADAD"))))
        self.assertTrue(any("superposition" in r for r in diagnostic(list("ADADADAD" * 2))))
        self.assertEqual(diagnostic(list("GG")), ["aucune ligne droite"])

    def test_rotations_gardent_la_forme(self):
        for m in EXEMPLES.values():
            for r in rotations(list(m)):
                self.assertTrue(circuit_convenable(r))
                self.assertEqual(sorted(r), sorted(m))


class GeometrieVariable(unittest.TestCase):
    def test_listes(self):
        c = list("AADADAADAD")
        seg = depuis_geometrie(c, [10, 20, 30, 40, 50, 60], [1, 2, 3, 4])
        self.assertEqual(seg[0], ("D", 30))
        self.assertEqual([x for k, x in seg if k == "V"], [1, 2, 3, 4])
        self.assertEqual(longueur(c, [10, 20, 30, 40, 50, 60]), 210)
        self.assertEqual(sum(x for k, x in seg if k == "D"), 210)

    def test_longueur_erronee(self):
        with self.assertRaises(ValueError):
            depuis_geometrie(list("ADADADAD"), [1, 2], 30)
        with self.assertRaises(ValueError):
            depuis_geometrie(list("ADADADAD"), 100, [1, 2, 3])

    def test_carte_segments(self):
        self.assertEqual(carte_segments(list("AADAGA")), [0, 0, 1, 2, 3, 4])
        c = list(EXEMPLES["en_L"])
        seg = depuis_geometrie(c, 100, 30)
        self.assertEqual(carte_segments(c)[-1], len(seg) - 1)


class Enumeration(unittest.TestCase):
    def test_polygones_fixes(self):
        self.assertEqual([nombre_polygones_fixes(n) for n in (4, 6, 8, 10, 12)],
                         [1, 2, 7, 28, 124])
        self.assertEqual(nombre_polygones_fixes(5), 0)
        self.assertEqual(nombre_polygones_fixes(2), 0)

    def test_formes_libres(self):
        self.assertEqual([len(circuits(n)) for n in (4, 6, 8, 10)], [1, 1, 3, 6])
        for n in (4, 6, 8, 10, 12):
            for c in circuits(n):
                self.assertEqual(c.count("A"), n)
                self.assertTrue(circuit_convenable(c), "".join(c))
        self.assertEqual(len({"".join(c) for c in circuits(10)}), 6)

    def test_cases(self):
        self.assertEqual(circuit_depuis_cases([(0, 0)]).count("A"), 4)
        for cases in FORMES.values():
            c = circuit_depuis_cases(cases)
            self.assertTrue(circuit_convenable(c))
            self.assertTrue(est_ferme(c))
        # périmètre d'un assemblage = nombre de lignes droites (5 cases en U : 12)
        self.assertEqual(circuit_depuis_cases(FORMES["en_U"]).count("A"), 12)

    def test_cases_invalides(self):
        for cases in ([], [(0, 0), (1, 1)], [(0, 0), (2, 0)],
                      [(x, y) for x in range(3) for y in range(3) if (x, y) != (1, 1)]):
            with self.assertRaises(ValueError):
                circuit_depuis_cases(cases)


class Profil(unittest.TestCase):
    def test_droites(self):
        for d, v1, v2 in [(1000, 0, 0), (500, 0, 0), (200, 30, 50), (150, 60, 20), (300, 100, 100)]:
            ph = pf.phases_droite(d, v1, v2)
            self.assertAlmostEqual(pf.duree(ph), temps_droite(d, v1, v2), places=9)
            self.assertAlmostEqual(pf.distance(ph), d, places=6)
            self.assertAlmostEqual(ph[0].va, v1)
            self.assertAlmostEqual(ph[-1].vb, v2)
            self.assertLessEqual(pf.vitesse_maximale_atteinte(ph), P.vmax + 1e-9)

    def test_droite_impossible(self):
        with self.assertRaises(ValueError):
            pf.phases_droite(50, 0, 60)

    def test_tour_et_course(self):
        for nom, m in EXEMPLES.items():
            seg = depuis_geometrie(list(m), 200, 30)
            for arc in (False, True):
                self.assertAlmostEqual(pf.duree(pf.phases_tour(seg, 0, 100, P, arc)),
                                       temps_tour(seg, 0, 100, P, arc), places=9)
                tours = pf.phases_course(seg, 4, P, arc)
                self.assertEqual(len(tours), 4)
                self.assertAlmostEqual(sum(pf.duree(t) for t in tours),
                                       temps_course(seg, 4, P, arc), places=9)

    def test_continuite_de_la_vitesse(self):
        seg = depuis_geometrie(list(EXEMPLES["en_L"]), 200, 30)
        phases = [ph for t in pf.phases_course(seg, 3) for ph in t]
        self.assertAlmostEqual(phases[0].va, 0)
        for a, b in zip(phases, phases[1:]):
            self.assertAlmostEqual(a.vb, b.va, places=9)

    def test_distance_avec_arcs(self):
        seg = depuis_geometrie(list("ADADADAD"), 200, 30)
        ph = pf.phases_tour(seg, 0, 100, P, True)
        self.assertAlmostEqual(pf.distance(ph), 800 + 4 * math.pi * 30 / 2, places=6)

    def test_echantillons(self):
        seg = depuis_geometrie(list("ADADADAD"), 200, 30)
        ech = pf.echantillons(pf.phases_tour(seg, 0, 100))
        self.assertEqual(ech[0], (0.0, 0.0, 0.0))
        ts = [e[0] for e in ech]
        self.assertEqual(ts, sorted(ts))

    def test_course_invalide(self):
        with self.assertRaises(ValueError):
            pf.phases_course([("D", 10)], 0)


class CinematiqueCorrigee(unittest.TestCase):
    def test_ligne_apres_virage_lent(self):
        seg = depuis_geometrie(list(EXEMPLES["rectangle"]), 200, 30)
        # la ligne suit un virage à 30 m : on ne peut pas la franchir à vmax
        self.assertAlmostEqual(vitesse_de_ligne(seg), vitesse_recommandee(30), places=6)

    def test_ligne_apres_droite_longue(self):
        seg = [("V", 500), ("D", 2000), ("V", 500), ("D", 2000)]
        self.assertAlmostEqual(vitesse_de_ligne(seg), P.vmax)

    def test_course_optimale_exacte(self):
        for m in EXEMPLES.values():
            seg = depuis_geometrie(list(m), 200, 30)
            for arc in (False, True):
                self.assertAlmostEqual(temps_course(seg, 3, P, arc),
                                       temps_tour(seg * 3, 0.0, P.vmax, P, arc))
            ts = [temps_course(seg, n, P, True) for n in range(1, 8)]
            incr = [b - a for a, b in zip(ts, ts[1:])]
            for x in incr[1:]:
                self.assertAlmostEqual(x, incr[1], places=6)
            self.assertGreaterEqual(incr[0], incr[1] - 1e-9)   # le départ arrêté coûte

    def test_vitesse_jamais_plus_grande_que_la_borne(self):
        seg = depuis_geometrie(list(EXEMPLES["en_L"]), 200, 30)
        for ph in [q for t in pf.phases_course(seg, 3) for q in t if q.nature == "virage"]:
            self.assertLessEqual(ph.va, vitesse_recommandee(30) + 1e-9)


class Analyses(unittest.TestCase):
    def test_distances(self):
        self.assertAlmostEqual(an.distance_acceleration(0, 100), 500)
        self.assertAlmostEqual(an.distance_freinage(100, 0), 250)
        self.assertAlmostEqual(an.rayon_limite(), 100)
        self.assertAlmostEqual(vitesse_recommandee(an.rayon_pour_vitesse(50)), 50)

    def test_temps_par_tour(self):
        seg = depuis_geometrie(list(EXEMPLES["carre"]), 200, 30)
        lap = an.temps_par_tour(seg, 5, P, True)
        self.assertAlmostEqual(sum(lap), temps_course(seg, 5, P, True))
        self.assertGreater(lap[0], lap[1])

    def test_meilleur_depart(self):
        c = list(EXEMPLES["en_L"])
        mot, t, essais = an.meilleur_depart(c, 200, 30, 3)
        self.assertEqual(t, min(e[1] for e in essais))
        self.assertLessEqual(t, temps_course(depuis_geometrie(c, 200, 30), 3, P, True))
        self.assertEqual(sorted(mot), sorted(c))

    def test_rayon_optimal_interieur(self):
        res = an.temps_selon_rayon(list("ADADADAD"), 200, [5, 10, 30, 60, 80, 100, 200], 5)
        meilleur = min(res, key=lambda x: x[1])[0]
        self.assertIn(meilleur, (60, 80))

    def test_parametres(self):
        base = temps_course(depuis_geometrie(list("ADADADAD"), 400, 30), 5, P, True)
        res = an.temps_selon_parametre(list("ADADADAD"), 400, 30, 5, "coeff_virage", [11], P)
        self.assertLess(res[0][1], base)
        # vmax jamais atteinte sur des droites de 200 m : aucun effet
        r = an.temps_selon_parametre(list("ADADADAD"), 200, 30, 5, "vmax", [80, 100, 120], P)
        self.assertAlmostEqual(r[0][1], r[2][1])

    def test_classement(self):
        cl = an.classement_formes(8, 200, 30, 5)
        self.assertEqual(len(cl), 3)
        self.assertEqual([x[1] for x in cl], sorted(x[1] for x in cl))
        self.assertEqual(cl[0][2], 4)                       # le plus rapide : 4 virages
        self.assertGreater(cl[-1][2], cl[0][2])

    def test_vitesse_moyenne_et_gain(self):
        v = an.vitesse_moyenne(list("ADADADAD"), 5, 200, 30)
        self.assertTrue(0 < v < P.vmax)
        depart, lance = an.gain_regime_etabli(list("ADADADAD"), 200, 30)
        self.assertGreater(depart, lance)


class Dessins(unittest.TestCase):
    def parse(self, svg):
        return ET.fromstring(svg)

    def test_svg_vitesse(self):
        for m in EXEMPLES.values():
            racine = self.parse(circuit_vitesse_svg(list(m), 200, 30, titre="t"))
            self.assertTrue(racine.tag.endswith("svg"))
        self.parse(circuit_vitesse_svg(list("AADADAADAD"), [200] * 6, [30, 30, 5, 30]))
        for cases in FORMES.values():
            self.parse(circuit_vitesse_svg(circuit_depuis_cases(cases), 100, 20))

    def test_svg_circuit_non_ferme(self):
        self.parse(circuit_vitesse_svg(list("AAGAAGA"), 100, 30, v0=10, vf=50))

    def test_svg_erreurs(self):
        with self.assertRaises(ValueError):
            circuit_vitesse_svg(list("GD"), 100, 30)
        with self.assertRaises(ValueError):
            circuit_vitesse_svg(list("AXA"), 100, 30)

    def test_graphe(self):
        self.parse(graphe_svg([("a", [(0, 0), (1, 2)]), ("b", [(0, 1), (1, 1)])], "t", "x", "y"))
        self.parse(graphe_svg([("", [(3, 5), (3, 5)])], "constant", "x", "y"))
        with self.assertRaises(ValueError):
            graphe_svg([("a", [])], "t", "x", "y")


class CasEtCli(unittest.TestCase):
    def test_chaque_cas(self):
        for nom in CAS:
            with tempfile.TemporaryDirectory() as d:
                _, sortie = silencieux(lancer, nom, Sortie(d))
                self.assertTrue(sortie.strip(), nom)
                for f in os.listdir(d):
                    ET.parse(os.path.join(d, f))
                if nom not in ("virages", "imposteurs"):
                    self.assertTrue(os.listdir(d), nom)

    def test_cli_cas_et_liste(self):
        code, sortie = silencieux(main, ["--liste"])
        self.assertEqual(code, 0)
        self.assertIn("enumeration", sortie)
        with tempfile.TemporaryDirectory() as d:
            code, sortie = silencieux(main, ["--cas", "droite", "--cas", "virage", "--sauver", d])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(os.path.join(d, "04_droite.svg")))

    def test_cli_enumerer(self):
        code, sortie = silencieux(main, ["--enumerer", "8"])
        self.assertEqual(code, 0)
        self.assertIn("7 polygones fixes, 3 formes", sortie)

    def test_cli_sorties_svg(self):
        with tempfile.TemporaryDirectory() as d:
            v, p = os.path.join(d, "v.svg"), os.path.join(d, "p.svg")
            code, sortie = silencieux(main, ["--exemple", "en_L", "--svg-vitesse", v, "--profil", p, "-n", "3"])
            self.assertEqual(code, 0)
            ET.parse(v), ET.parse(p)
            self.assertIn("Durée de chaque tour", sortie)

    def test_cli_erreurs(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                main([])
            self.assertEqual(main(["--enumerer", "7"]), 0)
            self.assertEqual(main(["AXA"]), 2)


if __name__ == "__main__":
    unittest.main()
