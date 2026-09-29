"""Profils de vitesse : ce que fait la voiture, instant par instant.

`cinematique` ne donne que des durées ; ici on reconstruit les phases du mouvement
(accélération à fond, palier à vmax, freinage à fond, virage à vitesse constante),
de sorte que la somme des durées redonne exactement `temps_tour` / `temps_course`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .cinematique import EPS, PAR, Parametres, _bornes


@dataclass(frozen=True)
class Phase:
    """Mouvement uniformément accéléré : v passe de `va` à `vb` en `dt` secondes."""
    nature: str        # "acceleration", "palier", "freinage" ou "virage"
    dt: float          # durée (s)
    ds: float          # distance parcourue (m)
    va: float          # vitesse au début (m/s)
    vb: float          # vitesse à la fin (m/s)
    segment: int       # indice du segment du circuit

    def vitesse(self, tau: float) -> float:
        """Vitesse au bout de tau secondes dans la phase."""
        return self.va + (self.vb - self.va) * (tau / self.dt if self.dt > 0 else 0.0)

    def distance(self, tau: float) -> float:
        """Distance parcourue au bout de tau secondes dans la phase."""
        return (self.va + self.vitesse(tau)) / 2 * tau


def phases_droite(d: float, v1: float, v2: float, p: Parametres = PAR,
                  segment: int = 0) -> list[Phase]:
    """Phases d'une ligne droite de longueur d, de v1 à v2 (mêmes hypothèses
    et mêmes erreurs que `temps_droite`)."""
    if d < 0 or not (0 <= v1 <= p.vmax + EPS) or not (0 <= v2 <= p.vmax + EPS):
        raise ValueError("paramètres hors domaine")
    a, f, vm = p.amax, p.fmax, p.vmax
    necessaire = (v2**2 - v1**2) / (2 * a) if v2 >= v1 else (v1**2 - v2**2) / (2 * f)
    if d < necessaire - EPS:
        raise ValueError("ligne droite trop courte pour passer de v1 à v2")
    d_acc = (vm**2 - v1**2) / (2 * a)
    d_frein = (vm**2 - v2**2) / (2 * f)
    if d >= d_acc + d_frein:
        v3, palier = vm, d - d_acc - d_frein
    else:
        v3sq = (2 * a * f * d + f * v1**2 + a * v2**2) / (a + f)
        v3, palier = max(math.sqrt(max(v3sq, 0.0)), v1, v2), 0.0
    phases = []
    if v3 > v1:
        phases.append(Phase("acceleration", (v3 - v1) / a, (v3**2 - v1**2) / (2 * a), v1, v3, segment))
    if palier > EPS:
        phases.append(Phase("palier", palier / v3, palier, v3, v3, segment))
    if v3 > v2:
        phases.append(Phase("freinage", (v3 - v2) / f, (v3**2 - v2**2) / (2 * f), v3, v2, segment))
    return phases


def phases_tour(c, v0: float, vf: float, p: Parametres = PAR,
                arc_virage: bool = True) -> list[Phase]:
    """Phases d'un tour parti à la vitesse v0 et fini à une vitesse <= vf.

    Même logique gloutonne que `temps_tour` : on accélère tant qu'on peut, en
    respectant les vitesses maximales d'entrée de chaque segment. Avec
    `arc_virage`, un virage est un quart de cercle de longueur πr/2 parcouru à
    vitesse constante ; sinon il est instantané (durée et longueur nulles)."""
    b = _bornes(c, vf, p)
    if v0 > b[0] + EPS:
        raise ValueError("vitesse de départ v0 trop élevée pour ce circuit")
    v, phases = v0, []
    for i, (kind, x) in enumerate(c):
        if kind == "V":
            if arc_virage:
                if v <= 0:
                    raise ValueError("vitesse nulle dans un virage")
                phases.append(Phase("virage", math.pi * x / 2 / v, math.pi * x / 2, v, v, i))
            continue
        v_sortie = min(b[i + 1], math.sqrt(v**2 + 2 * p.amax * x), p.vmax)
        phases.extend(phases_droite(x, v, v_sortie, p, i))
        v = v_sortie
    return phases


def phases_course(c, n: int, p: Parametres = PAR, arc_virage: bool = True) -> list[list[Phase]]:
    """Phases de chacun des n tours (même optimum exact que `temps_course` :
    le circuit est répété n fois, chaque tour part de la vitesse de fin du précédent)."""
    if n < 1:
        raise ValueError("n doit être >= 1")
    if not c:
        raise ValueError("circuit vide")
    m = len(c)
    tours: list[list[Phase]] = [[] for _ in range(n)]
    for ph in phases_tour(list(c) * n, 0.0, p.vmax, p, arc_virage):
        tours[ph.segment // m].append(Phase(ph.nature, ph.dt, ph.ds, ph.va, ph.vb, ph.segment % m))
    return tours


def duree(phases) -> float:
    return sum(ph.dt for ph in phases)


def distance(phases) -> float:
    return sum(ph.ds for ph in phases)


def echantillons(phases, par_phase: int = 16) -> list[tuple[float, float, float]]:
    """Points (t, s, v) le long des phases, pour tracer v(t) ou v(s)."""
    pts, t, s = [], 0.0, 0.0
    for ph in phases:
        n = 1 if ph.nature in ("palier", "virage") else par_phase
        if not pts:
            pts.append((t, s, ph.va))
        for k in range(1, n + 1):
            tau = ph.dt * k / n
            pts.append((t + tau, s + ph.distance(tau), ph.vitesse(tau)))
        t, s = t + ph.dt, s + ph.ds
    return pts


def vitesses_sur_segments(c, v0: float, vf: float, p: Parametres = PAR,
                          arc_virage: bool = True, par_phase: int = 12) -> dict[int, list[tuple[float, float]]]:
    """Pour chaque segment, la suite (position dans le segment en m, vitesse en m/s).

    Pour un virage la position va de 0 à πr/2 (vitesse constante). Sert à colorer
    un tracé selon la vitesse."""
    par_segment: dict[int, list[Phase]] = {}
    for ph in phases_tour(c, v0, vf, p, arc_virage):
        par_segment.setdefault(ph.segment, []).append(ph)
    res, v = {}, v0
    for i in range(len(c)):
        phs = par_segment.get(i)
        if phs:
            res[i] = [(s, vit) for _, s, vit in echantillons(phs, par_phase)]
            v = phs[-1].vb
        else:                                 # virage instantané
            res[i] = [(0.0, v)]
    return res


def vitesse_maximale_atteinte(phases) -> float:
    return max(max(ph.va, ph.vb) for ph in phases)
