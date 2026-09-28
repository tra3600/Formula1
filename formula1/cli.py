"""Interface en ligne de commande : python -m formula1 ..."""

from __future__ import annotations

import argparse
import sys

from .cinematique import Parametres, temps_course, vitesse_de_ligne
from .dessin import circuit_en_svg, dessine_circuit
from .geometrie import (circuit_convenable, contient_demi_tour, depuis_geometrie,
                        est_ferme, longueur, representation_minimale)

EXEMPLES = {
    "carre": "ADADADAD",
    "rectangle": "AADADAADAD",
    "en_L": "AAADADAAGADADAAD",
}


def analyser(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="formula1",
        description="Analyse un circuit à angles droits (A, G, D) et calcule "
                    "le temps de course minimal.")
    src = ap.add_mutually_exclusive_group(required=True)
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
    args = ap.parse_args(argv)
    if args.exemple:
        args.circuit = EXEMPLES[args.exemple]
    args.circuit = args.circuit.upper().replace(",", "").replace(" ", "")
    return args


def main(argv=None) -> int:
    args = analyser(argv)
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
    if args.svg:
        with open(args.svg, "w", encoding="utf-8") as f:
            f.write(circuit_en_svg(c))
        print(f"SVG écrit dans {args.svg}")
    if args.turtle:
        dessine_circuit(c)
    return 0
