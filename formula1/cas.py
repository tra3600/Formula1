"""Les cas illustrés du laboratoire Formula 1 : chaque fait affiché est calculé."""

from __future__ import annotations

import math
import os

from . import analyses as an
from .cinematique import PAR, Parametres, temps_course, temps_droite, vitesse_de_ligne, vitesse_recommandee
from .dessin import circuit_en_svg, circuit_vitesse_svg, graphe_svg
from .enumeration import circuit_depuis_cases, circuits, nombre_polygones_fixes
from .geometrie import (circuit_convenable, contient_demi_tour, depuis_geometrie, diagnostic,
                        est_ferme, longueur, representation_minimale, trajectoire)
from . import profil as pf

EXEMPLES = {
    "carre": "ADADADAD",
    "rectangle": "AADADAADAD",
    "en_L": "AAADADAAGADADAAD",
}

# assemblages de cases dont on longe le contour (voir circuit_depuis_cases)
FORMES = {
    "unite": [(0, 0)],
    "domino": [(0, 0), (1, 0)],
    "en_L_court": [(0, 0), (1, 0), (0, 1)],
    "serpent": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "en_U": [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1)],
    "escalier": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    "croix": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
}

D, R, TOURS = 200.0, 30.0, 5           # valeurs par défaut de la plupart des cas


# ----------------------------------------------------------------------
# Affichage
# ----------------------------------------------------------------------
class Sortie:
    """Enregistre les figures SVG dans un dossier (ou les ignore)."""

    def __init__(self, dossier: str | None = None):
        self.dossier = dossier
        self.vues = 0
        if dossier:
            os.makedirs(dossier, exist_ok=True)

    def svg(self, nom: str, contenu: str) -> None:
        if not self.dossier:
            self.vues += 1
            return
        chemin = os.path.join(self.dossier, f"{nom}.svg")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(contenu)
        print(f"   🖼  figure enregistrée : {chemin}")


def titre(texte: str) -> None:
    print("\n" + "═" * 72)
    print(f"  {texte}")
    print("═" * 72)


def para(texte: str) -> None:
    print(texte.strip("\n"))


def mot(c) -> str:
    return "".join(c)


def kmh(v: float) -> str:
    return f"{v * 3.6:.0f} km/h"


def seg_de(nom: str, d=D, r=R):
    return depuis_geometrie(list(EXEMPLES[nom]), d, r)


# ----------------------------------------------------------------------
# Les cas
# ----------------------------------------------------------------------
def cas_carre(out):
    titre("1. LE CARRÉ : un circuit, c'est un mot avec trois lettres")
    para("""
A = avancer d'une ligne droite, G = tourner à gauche, D = tourner à droite.
Le carré, c'est « avance, tourne à droite » quatre fois. Le programme sait
alors calculer sa longueur, vérifier qu'il boucle, et le dessiner.
""")
    c = list(EXEMPLES["carre"])
    print(f"   mot                : {mot(c)}")
    print(f"   trajectoire        : {trajectoire(c)}")
    print(f"   longueur (d=200 m) : {longueur(c, 200):g} m")
    print(f"   fermé ?            : {est_ferme(c)}    convenable ? {circuit_convenable(c)}")
    print("\nLes trois circuits prédéfinis :")
    for nom, m in EXEMPLES.items():
        cc = list(m)
        print(f"   {nom:<10} {m:<18} {longueur(cc, 200):>6g} m   {sum(e != 'A' for e in cc)} virages")
        out.svg(f"01_{nom}", circuit_en_svg(cc))


def cas_virages(out):
    titre("2. LES VIRAGES : « GGGG » ne sert à rien, « GG » est un demi-tour")
    para("""
Entre deux lignes droites, seul compte l'angle net (modulo 4 quarts de tour) :
GGGG = tour complet = rien ; GD = rien ; GGG = un seul D ; GG/DD = demi-tour,
interdit sur un circuit. `representation_minimale` réduit chaque suite de virages.
""")
    for m in ["AAGDGGGA", "AGGGGA", "AGGGA", "ADDDA", "AGDA", "AGGA", "AGDGGA", "GAAAG"]:
        c = list(m)
        print(f"   {m:<10} → minimale {mot(representation_minimale(c)) or '∅':<7} "
              f"demi-tour : {'oui' if contient_demi_tour(c) else 'non'}")
    print("\nNote : « GAAAG » a son demi-tour à cheval sur la fin et le début du mot ;")
    print("le circuit est cyclique, donc le programme le détecte aussi.")


def cas_imposteurs(out):
    titre("3. LES IMPOSTEURS : pourquoi ce circuit est refusé")
    para("""
Un circuit convenable est fermé, sans demi-tour, sans croisement ni
superposition. Pour chaque faux circuit, `diagnostic` donne la règle violée.
""")
    faux = {
        "ouvert": "AAGAAGA",
        "mauvais cap": "AGAGAGA",
        "demi-tour": "AGGA",
        "croisement (en huit)": "AAGAGAGAADADAD",
        "superposition (deux tours d'un coup)": "ADADADADADADADAD",
    }
    for nom, m in faux.items():
        c = list(m)
        raisons = diagnostic(c)
        print(f"\n   {nom} : {m}   convenable = {circuit_convenable(c)}")
        for r in raisons or ["(aucune : ce circuit est convenable)"]:
            print(f"      ✗ {r}")
    print("\n« Mauvais cap » revient bien au départ, mais tourné de 90° : la voiture ne")
    print("pourrait pas repartir. Et ADADADAD écrit deux fois repasse sur les mêmes arêtes :")
    print("deux tours d'un coup ne forment pas un nouveau circuit.")


def cas_droite(out):
    titre("4. UNE LIGNE DROITE : accélérer, tenir, freiner")
    para(f"""
Accélération max {PAR.amax:g} m/s², freinage max {PAR.fmax:g} m/s², vitesse max {PAR.vmax:g} m/s
({kmh(PAR.vmax)}). Sur une ligne droite de longueur d, entre v1 et v2, le plus
rapide est : accélérer à fond, tenir vmax si la ligne est assez longue, puis
freiner au dernier moment.
""")
    print(f"   0 → vmax : {an.distance_acceleration(0, PAR.vmax):g} m ;  vmax → 0 : "
          f"{an.distance_freinage(PAR.vmax, 0):g} m")
    print(f"\n   {'d (m)':>7}{'v1':>6}{'v2':>6}{'phases':>32}{'temps (s)':>12}{'v de pointe':>13}")
    cas = [(1000, 0, 0), (500, 0, 0), (300, 0, 0), (200, 30, 50), (150, 0, 50)]
    series = []
    for d, v1, v2 in cas:
        ph = pf.phases_droite(d, v1, v2)
        noms = " + ".join(f.nature[:4] for f in ph)
        t = temps_droite(d, v1, v2)
        assert abs(t - pf.duree(ph)) < 1e-9 and abs(pf.distance(ph) - d) < 1e-6
        print(f"   {d:>7}{v1:>6}{v2:>6}{noms:>32}{t:>12.3f}{pf.vitesse_maximale_atteinte(ph):>13.1f}")
        series.append((f"d={d} m ({v1}→{v2})", [(s, v) for _, s, v in pf.echantillons(ph)]))
    try:
        temps_droite(50, 0, 60)
    except ValueError as e:
        print(f"\n   d=50, 0 → 60 m/s : impossible ({e})")
    print(f"   distance minimale 0 → 60 m/s : {an.distance_acceleration(0, 60):g} m")
    out.svg("04_droite", graphe_svg(series[:4], "Vitesse sur une ligne droite", "distance (m)", "vitesse (m/s)", y0=0))


def cas_virage(out):
    titre("5. LE VIRAGE : la vitesse maximale dépend du rayon")
    para(f"""
Dans un virage de rayon r, la vitesse est limitée à vr(r) = 10·√r (et à vmax).
Au-delà de r = {an.rayon_limite():g} m, le virage n'est plus un obstacle.
""")
    print(f"   {'r (m)':>7}{'vr (m/s)':>11}{'vr (km/h)':>12}{'freinage depuis vmax (m)':>28}")
    for r in (4, 10, 30, 60, 100, 200):
        v = vitesse_recommandee(r)
        print(f"   {r:>7}{v:>11.1f}{v * 3.6:>12.0f}{an.distance_freinage(PAR.vmax, v):>28.0f}")
    print(f"\n   Rayon pour tenir 200 km/h : {an.rayon_pour_vitesse(200 / 3.6):.1f} m")
    pts = [(r, vitesse_recommandee(r) * 3.6) for r in range(1, 151)]
    out.svg("05_virage", graphe_svg([("vitesse en virage", pts)], "Vitesse maximale selon le rayon",
                                    "rayon (m)", "km/h", y0=0))


def cas_course(out):
    titre("6. LA COURSE : le premier tour est le plus long")
    para("""
Départ arrêté, arrivée libre. Pour n tours, le circuit est répété n fois bout à
bout et la voiture accélère dès qu'elle le peut, freine au dernier moment.
Aux tours suivants elle repart à la vitesse de sortie du tour précédent.
""")
    for nom in EXEMPLES:
        c = list(EXEMPLES[nom])
        seg = depuis_geometrie(c, D, R)
        s = vitesse_de_ligne(seg)
        lap = an.temps_par_tour(seg, TOURS, PAR, True)
        print(f"\n   {nom} ({mot(c)}) : franchissement de la ligne à {kmh(s)}")
        print("      tours :", "  ".join(f"{t:.2f}" for t in lap), "s")
        print(f"      total {TOURS} tours : {temps_course(seg, TOURS, PAR, True):.2f} s "
              f"(sans compter les virages : {temps_course(seg, TOURS):.2f} s)")
        print(f"      vitesse moyenne : {an.vitesse_moyenne(c, TOURS, D, R) * 3.6:.0f} km/h")
    print("\nCorrection apportée : la ligne d'arrivée suit un virage lent ; la voiture ne peut")
    print("donc pas la franchir à vmax. Le temps est maintenant l'optimum exact sur n tours")
    print("répétés, et non plus un régime établi supposé à vmax.")
    seg = seg_de("en_L")
    out.svg("06_temps_tours", graphe_svg([("temps total", an.temps_selon_tours(seg, range(1, 11)))],
                                         "Temps de course (circuit en L)", "tours", "temps (s)", y0=0))


def cas_profil(out):
    titre("7. LE PROFIL DE VITESSE : v(t) et v(s) sur plusieurs tours")
    para("""
On reconstruit les phases du mouvement : accélération, palier, freinage, virage à
vitesse constante. La somme des durées redonne exactement le temps de course.
""")
    seg = seg_de("rectangle")
    tours = pf.phases_course(seg, 3)
    tout = [ph for t in tours for ph in t]
    print(f"   rectangle, 3 tours : {len(tout)} phases ; durée {pf.duree(tout):.4f} s "
          f"(temps_course = {temps_course(seg, 3, PAR, True):.4f} s)")
    print(f"   distance parcourue : {pf.distance(tout):.1f} m ; vitesse de pointe : "
          f"{kmh(pf.vitesse_maximale_atteinte(tout))}")
    nat = {}
    for ph in tout:
        nat[ph.nature] = nat.get(ph.nature, 0.0) + ph.dt
    for k, v in nat.items():
        print(f"      {k:<13}: {v:6.2f} s ({100 * v / pf.duree(tout):4.1f} %)")
    ech = pf.echantillons(tout)
    out.svg("07_profil_temps", graphe_svg([("v(t)", [(t, v * 3.6) for t, s, v in ech])],
                                          "Vitesse au cours du temps (rectangle, 3 tours)",
                                          "temps (s)", "km/h", y0=0))
    out.svg("07_profil_distance", graphe_svg([("v(s)", [(s, v * 3.6) for t, s, v in ech])],
                                             "Vitesse selon la distance (rectangle, 3 tours)",
                                             "distance (m)", "km/h", y0=0))


def cas_vitesse(out):
    titre("8. LE CIRCUIT EN COULEURS : où va-t-on vite ?")
    para("""
Chaque tronçon du tracé est coloré par la vitesse en régime établi (bleu = lent,
rouge = 360 km/h). On lit la stratégie : freinages tardifs avant les virages,
pleine accélération en sortie.
""")
    for nom in EXEMPLES:
        seg = seg_de(nom)
        s = vitesse_de_ligne(seg)
        print(f"   {nom:<10} ligne à {kmh(s)} ; virage à {kmh(vitesse_recommandee(R))}")
        out.svg(f"08_vitesse_{nom}", circuit_vitesse_svg(list(EXEMPLES[nom]), D, R,
                                                          titre=f"{nom} : vitesse en régime établi"))


def cas_rayon(out):
    titre("9. LE RAYON OPTIMAL : virages serrés ou larges ?")
    para("""
Un grand rayon autorise une vitesse plus élevée... mais rallonge le virage
(quart de cercle de longueur πr/2). Il existe donc un rayon optimal.
""")
    c = list(EXEMPLES["carre"])
    rayons = [5, 10, 20, 30, 45, 60, 80, 100, 150, 200]
    res = an.temps_selon_rayon(c, D, rayons, TOURS)
    print(f"   {'r (m)':>7}{'temps (s)':>12}")
    for r, t in res:
        print(f"   {r:>7}{t:>12.2f}")
    fin = an.temps_selon_rayon(c, D, [r / 2 for r in range(4, 400)], TOURS)
    r_opt, t_opt = min(fin, key=lambda x: x[1])
    print(f"\n   Optimum (pas de 0,5 m) : r ≈ {r_opt:g} m → {t_opt:.2f} s "
          f"(vitesse en virage {kmh(vitesse_recommandee(r_opt))})")
    out.svg("09_rayon", graphe_svg([("carré 200 m", fin)], "Temps de course selon le rayon des virages",
                                   "rayon (m)", "temps (s)"))


def cas_reglages(out):
    titre("10. LES RÉGLAGES : quelle amélioration de la voiture rapporte le plus ?")
    para("""
On augmente de 10 % un paramètre à la fois et on regarde le temps gagné.
Un paramètre inutile (jamais atteint) ne fait rien gagner : c'est aussi une
information !
""")
    for nom in ("carre", "en_L"):
        seg = seg_de(nom, 400, R)
        base = temps_course(seg, TOURS, PAR, True)
        print(f"\n   {nom} (lignes de 400 m) : {base:.2f} s")
        for champ, libelle in (("amax", "accélération"), ("fmax", "freinage"),
                               ("vmax", "vitesse max"), ("coeff_virage", "adhérence en virage")):
            q = Parametres(**{**PAR.__dict__, champ: getattr(PAR, champ) * 1.1})
            t = temps_course(seg, TOURS, q, True)
            print(f"      +10 % {libelle:<20}: {t:8.2f} s ({100 * (t - base) / base:+5.1f} %)")
    seg = seg_de("carre", 400, R)
    series = [(f"{nom}", an.temps_selon_parametre(list(EXEMPLES["carre"]), 400, R, TOURS, nom,
                                                  [PAR.__dict__[nom] * k / 10 for k in range(6, 17)]))
              for nom in ("amax", "fmax", "vmax", "coeff_virage")]
    series = [(n, [(v / PAR.__dict__[n], t) for v, t in pts]) for n, pts in series]
    out.svg("10_reglages", graphe_svg(series, "Temps de course selon chaque réglage (facteur ×)",
                                      "facteur appliqué au paramètre", "temps (s)"))


def cas_depart(out):
    titre("11. LA LIGNE DE DÉPART : où la placer ?")
    para("""
Partir de l'arrêt au milieu d'une grande droite n'est pas partir devant un virage.
Un circuit fermé peut être « coupé » n'importe où : on essaie tous les
décalages du mot et on garde le plus rapide.
""")
    for nom in ("rectangle", "en_L"):
        c = list(EXEMPLES[nom])
        best, t, essais = an.meilleur_depart(c, D, R, 3)
        pire = max(essais, key=lambda e: e[1])
        print(f"\n   {nom} ({mot(c)}), 3 tours")
        print(f"      départ tel quel      : {temps_course(depuis_geometrie(c, D, R), 3, PAR, True):.2f} s")
        print(f"      meilleure position   : {mot(best)} → {t:.2f} s")
        print(f"      pire position        : {mot(pire[0])} → {pire[1]:.2f} s")
        out.svg(f"11_depart_{nom}", circuit_vitesse_svg(best, D, R, titre=f"{nom} : meilleure ligne de départ"))


def cas_variable(out):
    titre("12. GÉOMÉTRIE VARIABLE : chicanes, épingles et grandes courbes")
    para("""
Les longueurs de droites et les rayons peuvent différer d'un endroit à l'autre :
on passe alors des listes à `depuis_geometrie`. Un seul virage serré (une
« épingle ») suffit à dicter la stratégie de tout le tour.
""")
    c = list(EXEMPLES["rectangle"])
    variantes = {
        "uniforme (30 m)": ([200] * 6, [30] * 4),
        "une épingle (5 m)": ([200] * 6, [30, 30, 5, 30]),
        "grandes courbes (100 m)": ([200] * 6, [100] * 4),
        "longue ligne droite": ([200, 200, 100, 800, 100, 200], [30] * 4),
    }
    for nom, (ds, rs) in variantes.items():
        seg = depuis_geometrie(c, ds, rs)
        print(f"   {nom:<26} longueur {longueur(c, ds):>5g} m   ligne à {kmh(vitesse_de_ligne(seg)):>8}"
              f"   {TOURS} tours : {temps_course(seg, TOURS, PAR, True):7.2f} s")
    out.svg("12_epingle", circuit_vitesse_svg(c, [200] * 6, [30, 30, 5, 30],
                                              titre="rectangle avec une épingle de 5 m"))


def cas_enumeration(out):
    titre("13. TOUS LES CIRCUITS POSSIBLES : combien y en a-t-il ? lequel est le plus rapide ?")
    para("""
Un circuit convenable à n lignes droites est un polygone fermé sans point double
sur la grille. On les énumère tous ; « fixes » = à translation près, « formes » =
à rotation et symétrie près (les vrais circuits différents).
""")
    print(f"   {'n droites':>10}{'fixes':>8}{'formes':>8}{'plus rapide':>26}{'plus lent':>26}")
    for n in (4, 6, 8, 10, 12):
        cl = an.classement_formes(n, D, R, TOURS)
        rapide, lent = cl[0], cl[-1]
        print(f"   {n:>10}{nombre_polygones_fixes(n):>8}{len(cl):>8}"
              f"{rapide[1]:>17.1f} s ({rapide[2]:>2} v.){lent[1]:>13.1f} s ({lent[2]:>2} v.)")
    print("\n   Les fixes valent 1, 2, 7, 28, 124 : ce sont les polygones auto-évitants.")
    print("   Constat : le plus rapide a le moins de virages (4) et les plus longues droites")
    print("   (un rectangle étiré) ; le plus lent est celui qui en a le plus.")
    cl = an.classement_formes(8, D, R, TOURS)
    for k, (m, t, nv) in enumerate(cl, 1):
        print(f"      n=8, rang {k} : {mot(m)} ({nv} virages) {t:.1f} s")
        out.svg(f"13_forme8_rang{k}", circuit_vitesse_svg(m, D, R, titre=f"8 droites, rang {k} : {t:.1f} s"))
    tous = an.classement_formes(10, D, R, TOURS)
    out.svg("13_classement_10", graphe_svg([("temps (s)", [(k, t) for k, (_, t, _) in enumerate(tous, 1)])],
                                            "Circuits à 10 droites, du plus rapide au plus lent",
                                            "rang", "temps (s)"))


def cas_formes(out):
    titre("14. DES CASES AU CIRCUIT : longer le contour d'un assemblage")
    para("""
Longer le contour d'un polyomino (assemblage de cases carrées) donne un circuit
convenable. Le programme transforme les cases en mot A/G/D, puis chronomètre.
""")
    print(f"   {'forme':<12}{'cases':>6}{'droites':>9}{'virages':>9}{'temps (s)':>12}")
    for nom, cases in FORMES.items():
        c = circuit_depuis_cases(cases)
        assert circuit_convenable(c)
        t = temps_course(depuis_geometrie(c, D, R), TOURS, PAR, True)
        print(f"   {nom:<12}{len(cases):>6}{c.count('A'):>9}{len(c) - c.count('A'):>9}{t:>12.2f}")
        out.svg(f"14_{nom}", circuit_vitesse_svg(c, D, R, titre=nom))
    try:
        circuit_depuis_cases([(0, 0), (1, 1)])
    except ValueError as e:
        print(f"\n   Deux cases qui se touchent par un coin : refusé ({e}).")


CAS = {
    "carre": (cas_carre, "le mot A/G/D, longueur, fermeture, dessin"),
    "virages": (cas_virages, "représentation minimale, demi-tours"),
    "imposteurs": (cas_imposteurs, "faux circuits et règle violée"),
    "droite": (cas_droite, "accélération, palier, freinage sur une droite"),
    "virage": (cas_virage, "vitesse maximale selon le rayon"),
    "course": (cas_course, "temps par tour, départ arrêté"),
    "profil": (cas_profil, "v(t) et v(s) sur plusieurs tours"),
    "vitesse": (cas_vitesse, "circuit coloré par la vitesse"),
    "rayon": (cas_rayon, "rayon optimal des virages"),
    "reglages": (cas_reglages, "quel réglage de la voiture rapporte le plus"),
    "depart": (cas_depart, "meilleure position de la ligne de départ"),
    "variable": (cas_variable, "épingles, chicanes, longueurs variables"),
    "enumeration": (cas_enumeration, "tous les circuits d'une taille donnée, classés"),
    "formes": (cas_formes, "du polyomino au circuit"),
}


def lancer(nom: str, sortie: Sortie) -> None:
    CAS[nom][0](sortie)


def liste() -> None:
    print("Cas disponibles :")
    for nom, (_, desc) in CAS.items():
        print(f"   {nom:<12} {desc}")
