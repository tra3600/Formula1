"""Temps de parcours minimal d'un circuit.

Un circuit cinématique est une liste de segments :
  ("D", d) : ligne droite de longueur d (m)
  ("V", r) : virage de rayon r (m), pris à vitesse constante <= vitesse_recommandee(r)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

EPS = 1e-9


@dataclass(frozen=True)
class Parametres:
    amax: float = 10.0   # accélération maximale (m/s²)
    fmax: float = 20.0   # freinage maximal, en valeur absolue (m/s²)
    vmax: float = 100.0  # vitesse maximale (m/s)
    coeff_virage: float = 10.0  # vr(r) = coeff_virage * sqrt(r)


PAR = Parametres()


def vitesse_recommandee(r: float, p: Parametres = PAR) -> float:
    """Vitesse maximale dans un virage de rayon r."""
    return min(p.vmax, p.coeff_virage * math.sqrt(r))


def _valider(c) -> None:
    for seg in c:
        if len(seg) != 2 or seg[0] not in ("D", "V") or seg[1] < 0:
            raise ValueError(f"segment invalide : {seg!r} (attendu ('D', d) ou ('V', r))")


def _bornes(c, vf: float, p: Parametres) -> list[float]:
    """Vitesses maximales aux n+1 frontières des segments (dernier = vf)."""
    _valider(c)
    if not 0 <= vf <= p.vmax:
        raise ValueError("vf doit être dans [0, vmax]")
    b = [0.0] * (len(c) + 1)
    b[-1] = vf
    for i in range(len(c) - 1, -1, -1):
        kind, x = c[i]
        if kind == "V":
            b[i] = min(b[i + 1], vitesse_recommandee(x, p))
        else:  # freiner sur toute la ligne droite
            b[i] = min(p.vmax, math.sqrt(b[i + 1] ** 2 + 2 * p.fmax * x))
    return b


def vitesses_entree_max(c, vf: float, p: Parametres = PAR) -> list[float]:
    """Vitesse maximale à l'entrée de chaque segment, sachant que la vitesse
    en fin de circuit ne doit pas dépasser vf."""
    return _bornes(c, vf, p)[:-1]


def temps_droite(d: float, v1: float, v2: float, p: Parametres = PAR) -> float:
    """Temps minimal pour parcourir une ligne droite de longueur d en entrant
    à la vitesse v1 et en sortant à v2. ValueError si c'est impossible."""
    if d < 0 or not (0 <= v1 <= p.vmax + EPS) or not (0 <= v2 <= p.vmax + EPS):
        raise ValueError("paramètres hors domaine")
    a, f, vm = p.amax, p.fmax, p.vmax
    if v2 >= v1:
        necessaire = (v2**2 - v1**2) / (2 * a)
    else:
        necessaire = (v1**2 - v2**2) / (2 * f)
    if d < necessaire - EPS:
        raise ValueError("ligne droite trop courte pour passer de v1 à v2")
    d_acc = (vm**2 - v1**2) / (2 * a)
    d_frein = (vm**2 - v2**2) / (2 * f)
    if d >= d_acc + d_frein:  # palier à vmax
        return (vm - v1) / a + (vm - v2) / f + (d - d_acc - d_frein) / vm
    # vitesse de pointe intermédiaire v3 < vmax
    v3sq = (2 * a * f * d + f * v1**2 + a * v2**2) / (a + f)
    v3 = max(math.sqrt(max(v3sq, 0.0)), v1, v2)
    return (v3 - v1) / a + (v3 - v2) / f


def _simuler_tour(c, v0: float, vf: float, p: Parametres, arc_virage: bool):
    """(durée, vitesse finale) d'un tour glouton : on accélère dès qu'on le peut,
    sans dépasser les vitesses d'entrée maximales de chaque segment."""
    b = _bornes(c, vf, p)
    if v0 > b[0] + EPS:
        raise ValueError("vitesse de départ v0 trop élevée pour ce circuit")
    v = v0
    total = 0.0
    for i, (kind, x) in enumerate(c):
        if kind == "V":
            if arc_virage:
                if v <= 0:
                    raise ValueError("vitesse nulle dans un virage")
                total += math.pi * x / 2 / v
            continue
        atteignable = math.sqrt(v**2 + 2 * p.amax * x)
        v_sortie = min(b[i + 1], atteignable, p.vmax)
        total += temps_droite(x, v, v_sortie, p)
        v = v_sortie
    return total, v


def temps_tour(c, v0: float, vf: float, p: Parametres = PAR,
               arc_virage: bool = False) -> float:
    """Temps minimal d'un tour, parti à la vitesse v0 et fini à une vitesse <= vf.
    Si arc_virage, chaque virage est un quart de cercle parcouru à vitesse
    constante ; sinon sa durée est négligée."""
    return _simuler_tour(c, v0, vf, p, arc_virage)[0]


def vitesse_de_ligne(c, p: Parametres = PAR) -> float:
    """Vitesse maximale s à laquelle on peut franchir la ligne à chaque tour en
    régime permanent : s doit pouvoir être freinée jusqu'au bout du tour ET être
    effectivement retrouvée à la fin du tour précédent (une ligne juste après un
    virage lent ne se franchit pas à vmax)."""
    s = p.vmax
    for _ in range(5000):
        nouveau = min(s, _bornes(c, s, p)[0])
        if nouveau >= s - EPS:
            fin = _simuler_tour(c, s, s, p, False)[1]
            nouveau = min(s, fin)
            if nouveau >= s - EPS:
                return s
        s = nouveau
    return s


def temps_course(c, n: int, p: Parametres = PAR, arc_virage: bool = False) -> float:
    """Temps minimal pour n tours, départ arrêté, vitesse finale libre.

    Optimum exact : le circuit est répété n fois bout à bout, la voiture accélère
    dès qu'elle le peut et freine au dernier moment (ce qui inclut le régime
    établi des tours intermédiaires)."""
    if n < 1:
        raise ValueError("n doit être >= 1")
    if not c:
        raise ValueError("circuit vide")
    return temps_tour(list(c) * n, 0.0, p.vmax, p, arc_virage)
