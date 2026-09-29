"""Extrapolations : que devient le temps de course quand on change le circuit,
la voiture ou la ligne de départ ?"""

from __future__ import annotations

import math

from .cinematique import PAR, Parametres, temps_course, temps_tour, vitesse_de_ligne
from .enumeration import circuits
from .geometrie import depuis_geometrie, rotations


# ----------------------------------------------------------------------
# Distances caractéristiques
# ----------------------------------------------------------------------
def distance_acceleration(v1: float, v2: float, p: Parametres = PAR) -> float:
    """Distance minimale pour passer de v1 à v2 > v1 à pleine accélération."""
    return (v2**2 - v1**2) / (2 * p.amax)


def distance_freinage(v1: float, v2: float, p: Parametres = PAR) -> float:
    """Distance minimale pour passer de v1 à v2 < v1 à pleine décélération."""
    return (v1**2 - v2**2) / (2 * p.fmax)


def rayon_limite(p: Parametres = PAR) -> float:
    """Rayon à partir duquel un virage ne limite plus la vitesse (vr(r) = vmax)."""
    return (p.vmax / p.coeff_virage) ** 2


def rayon_pour_vitesse(v: float, p: Parametres = PAR) -> float:
    """Rayon dont la vitesse recommandée vaut v."""
    return (v / p.coeff_virage) ** 2


# ----------------------------------------------------------------------
# Structure d'une course
# ----------------------------------------------------------------------
def temps_par_tour(c, n: int, p: Parametres = PAR, arc_virage: bool = False) -> list[float]:
    """Durée de chacun des n tours de la course optimale (départ arrêté)."""
    cumul = [temps_course(c, k, p, arc_virage) for k in range(1, n + 1)]
    return [cumul[0]] + [b - a for a, b in zip(cumul, cumul[1:])]


def meilleur_depart(c_ferme, d, r, n: int, p: Parametres = PAR, arc_virage: bool = True):
    """Où placer la ligne de départ ? Essaie tous les décalages du mot A/G/D.

    Retourne (mot, temps, liste de (mot, temps)) pour la meilleure position."""
    essais = []
    for mot in rotations(c_ferme):
        try:
            t = temps_course(depuis_geometrie(mot, d, r), n, p, arc_virage)
        except ValueError:
            continue
        essais.append((mot, t))
    meilleur = min(essais, key=lambda e: e[1])
    return meilleur[0], meilleur[1], essais


# ----------------------------------------------------------------------
# Balayages de paramètres
# ----------------------------------------------------------------------
def temps_selon_rayon(c, d: float, rayons, n: int, p: Parametres = PAR,
                      arc_virage: bool = True) -> list[tuple[float, float]]:
    return [(r, temps_course(depuis_geometrie(c, d, r), n, p, arc_virage)) for r in rayons]


def temps_selon_longueur(c, longueurs, r: float, n: int, p: Parametres = PAR,
                         arc_virage: bool = True) -> list[tuple[float, float]]:
    return [(d, temps_course(depuis_geometrie(c, d, r), n, p, arc_virage)) for d in longueurs]


def temps_selon_parametre(c, d: float, r: float, n: int, nom: str, valeurs,
                          p: Parametres = PAR, arc_virage: bool = True) -> list[tuple[float, float]]:
    """Fait varier un paramètre de la voiture ("amax", "fmax", "vmax", "coeff_virage")."""
    res = []
    for v in valeurs:
        q = Parametres(**{**p.__dict__, nom: v})
        res.append((v, temps_course(depuis_geometrie(c, d, r), n, q, arc_virage)))
    return res


def temps_selon_tours(c, tours, p: Parametres = PAR, arc_virage: bool = True):
    return [(n, temps_course(c, n, p, arc_virage)) for n in tours]


# ----------------------------------------------------------------------
# Quelle forme de circuit est la plus rapide ?
# ----------------------------------------------------------------------
def classement_formes(n_droites: int, d: float, r: float, n_tours: int,
                      p: Parametres = PAR, arc_virage: bool = True):
    """Toutes les formes de circuits convenables à n_droites lignes droites,
    triées du plus rapide au plus lent ; chaque forme est chronométrée depuis
    sa meilleure ligne de départ. Retourne [(mot_optimal, temps, nb_virages)]."""
    lignes = []
    for mot in circuits(n_droites):
        best, t, _ = meilleur_depart(mot, d, r, n_tours, p, arc_virage)
        lignes.append((best, t, sum(1 for e in mot if e != "A")))
    lignes.sort(key=lambda x: x[1])
    return lignes


def vitesse_moyenne(c, n: int, d, r, p: Parametres = PAR, arc_virage: bool = True) -> float:
    """Vitesse moyenne (m/s) sur n tours : longueur parcourue / durée."""
    seg = depuis_geometrie(c, d, r)
    longueur = sum(x if k == "D" else (math.pi * x / 2 if arc_virage else 0.0) for k, x in seg)
    return n * longueur / temps_course(seg, n, p, arc_virage)


def gain_regime_etabli(c, d, r, p: Parametres = PAR, arc_virage: bool = True) -> tuple[float, float]:
    """(tour 1 départ arrêté, tour lancé en régime établi) : ce que coûte le départ."""
    seg = depuis_geometrie(c, d, r)
    s = vitesse_de_ligne(seg, p)
    return (temps_tour(seg, 0.0, s, p, arc_virage), temps_tour(seg, s, s, p, arc_virage))
