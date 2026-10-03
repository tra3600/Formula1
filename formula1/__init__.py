"""Modélisations autour de la Formule 1 (sujet Centrale-Supélec info 2022).

Modules : geometrie, cinematique, profil, analyses, enumeration, dessin, cas, cli."""

from .cinematique import (
    Parametres,
    temps_course,
    temps_droite,
    temps_tour,
    vitesse_recommandee,
    vitesses_entree_max,
)
from .geometrie import (
    circuit_convenable,
    contient_demi_tour,
    depuis_geometrie,
    est_ferme,
    longueur,
    representation_minimale,
    trajectoire,
)
from .dessin import circuit_en_svg, circuit_vitesse_svg, dessine_circuit, graphe_svg
from .enumeration import circuit_depuis_cases, circuits, nombre_polygones_fixes
from .geometrie import diagnostic

__all__ = [
    "Parametres", "temps_course", "temps_droite", "temps_tour",
    "vitesse_recommandee", "vitesses_entree_max", "circuit_convenable",
    "contient_demi_tour", "depuis_geometrie", "est_ferme", "longueur",
    "representation_minimale", "trajectoire", "dessine_circuit",
    "circuit_en_svg", "circuit_vitesse_svg", "graphe_svg", "circuit_depuis_cases",
    "circuits", "nombre_polygones_fixes", "diagnostic",
]
