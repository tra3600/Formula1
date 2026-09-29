"""Interface en ligne de commande : python -m formula1 ..."""

from __future__ import annotations

import argparse
import sys

from .cinematique import Parametres, temps_course
from .dessin import circuit_en_svg, dessine_circuit
from .geometrie import (circuit_convenable, contient_demi_tour, depuis_geometrie,
                        est_ferme, longueur, representation_minimale)

from .cas import CAS, EXEMPLES, Sortie, lancer, liste
from .cinematique import vitesse_de_ligne
from .dessin import circuit_vitesse_svg, graphe_svg
from . import profil as pf


def analyser(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="formula1",
        description="Analyse un circuit à angles droits (A, G, D) et calcule "
                    "le temps de course minimal.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("circuit", nargs="?", help="ex. AGAGAGAG (A avancer, G gauche, D droite)")
    src.add_argument("--exemple", choices=sorted(EXEMPLES), help="circuit prédéfini")
    ap.add_argument("-l", "--longueur", type=float, default=200, help="longueur d'une ligne droite (m)")
    ap.add_argument("-r", "--rayon", type=float, default=30, help="rayon des virages (m)")
    ap.add_argument("-n", "--tours", type=int, default=5, help="nombre de tours")
    ap.add_argument("--amax", type=float, default=10, help="accélération max (m/s²)")
    ap.add_argument("--fmax", type=float, default=20, help="freinage max, valeur absolue (m/s²)")
    ap.add_argument("--vmax", type=float, default=100, help="vitesse max (m/s)")
    ap.add_argument("--arc", action="store_true", help="compter la durée des virages (quart de cercle)")
    ap.add_argument("--svg", metavar="FICHIER", help="exporte le tracé en SVG")
    ap.add_argument("--turtle", action="store_true", help="dessine avec turtle")
    ap.add_argument("--svg-vitesse", metavar="FICHIER", help="tracé coloré par la vitesse (SVG)")
    ap.add_argument("--profil", metavar="FICHIER", help="profil de vitesse v(t) sur tous les tours (SVG)")
    lab = ap.add_argument_group("laboratoire (cas illustrés)")
    lab.add_argument("--cas", action="append", choices=list(CAS), help="cas illustré (répétable)")
    lab.add_argument("--tout", action="store_true", help="tous les cas illustrés")
    lab.add_argument("--liste", action="store_true", help="liste les cas illustrés")
    lab.add_argument("--sauver", metavar="DOSSIER", help="enregistre les figures SVG des cas")
    lab.add_argument("--enumerer", type=int, metavar="N",
                     help="liste les circuits convenables à N lignes droites, du plus rapide au plus lent")
    args = ap.parse_args(argv)
    if not (args.circuit or args.exemple or args.cas or args.tout or args.liste or args.enumerer):
        ap.error("donner un circuit, --exemple, --cas, --tout, --liste ou --enumerer")
    if args.exemple:
        args.circuit = EXEMPLES[args.exemple]
    if args.circuit:
        args.circuit = args.circuit.upper().replace(",", "").replace(" ", "")
    return args


def main(argv=None) -> int:
    args = analyser(argv)
    if args.liste:
        liste()
    if args.tout or args.cas:
        sortie = Sortie(args.sauver)
        for nom in (list(CAS) if args.tout else args.cas):
            lancer(nom, sortie)
        if not args.sauver and sortie.vues:
            print(f"\n({sortie.vues} figures non enregistrées : ajoute --sauver DOSSIER)")
    if args.enumerer:
        _enumerer(args)
    if not args.circuit:
        return 0
    c = list(args.circuit)
    try:
        ferme = est_ferme(c)
        conv = circuit_convenable(c)
    except ValueError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 2
    print(f"Circuit               : {args.circuit}")
    print(f"Représentation minimale : {''.join(representation_minimale(c))}")
    print(f"Longueur totale       : {longueur(c, args.longueur):g} m")
    print(f"Fermé                 : {'oui' if ferme else 'non'}")
    print(f"Demi-tour             : {'oui' if contient_demi_tour(c) else 'non'}")
    print(f"Convenable            : {'oui' if conv else 'non'}")
    if not conv:
        print("Le circuit n'est pas convenable : pas de calcul de temps.")
    else:
        p = Parametres(args.amax, args.fmax, args.vmax)
        seg = depuis_geometrie(c, args.longueur, args.rayon)
        t = temps_course(seg, args.tours, p, args.arc)
        print(f"Vitesse de passage    : {vitesse_de_ligne(seg, p) * 3.6:.1f} km/h")
        print(f"Temps ({args.tours} tours)      : {t:.2f} s")
        if args.tours > 1:
            from .analyses import temps_par_tour
            tp = temps_par_tour(seg, args.tours, p, args.arc)
            print("Durée de chaque tour  : " + "  ".join(f"{x:.2f}" for x in tp) + " s")
    if args.svg:
        with open(args.svg, "w", encoding="utf-8") as f:
            f.write(circuit_en_svg(c))
        print(f"SVG écrit dans {args.svg}")
    if conv and args.svg_vitesse:
        with open(args.svg_vitesse, "w", encoding="utf-8") as f:
            f.write(circuit_vitesse_svg(c, args.longueur, args.rayon, p, titre=args.circuit))
        print(f"SVG (vitesse) écrit dans {args.svg_vitesse}")
    if conv and args.profil:
        ech = pf.echantillons([ph for t in pf.phases_course(seg, args.tours, p, True) for ph in t])
        with open(args.profil, "w", encoding="utf-8") as f:
            f.write(graphe_svg([("v(t)", [(t, v * 3.6) for t, _, v in ech])],
                               f"Vitesse sur {args.tours} tours", "temps (s)", "km/h", y0=0))
        print(f"Profil de vitesse écrit dans {args.profil}")
    if args.turtle:
        dessine_circuit(c)
    return 0


def _enumerer(args) -> None:
    from .analyses import classement_formes
    from .enumeration import nombre_polygones_fixes
    n = args.enumerer
    if n < 4 or n % 2:
        print("Erreur : un circuit fermé a un nombre pair (>= 4) de lignes droites.", file=sys.stderr)
        return
    cl = classement_formes(n, args.longueur, args.rayon, args.tours,
                           Parametres(args.amax, args.fmax, args.vmax), args.arc)
    print(f"{nombre_polygones_fixes(n)} polygones fixes, {len(cl)} formes à {n} droites "
          f"(l = {args.longueur:g} m, r = {args.rayon:g} m, {args.tours} tours) :")
    for k, (m, t, nv) in enumerate(cl, 1):
        print(f"  {k:>3}. {''.join(m):<40} {nv:>2} virages  {t:8.2f} s")
