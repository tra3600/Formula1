"""Énumération de tous les circuits convenables ayant un nombre donné de lignes droites.

Un circuit convenable à `n` "A" est un polygone fermé sans point double sur la
grille (une « marche auto-évitante fermée ») de n arêtes. On les énumère par
recherche en profondeur, puis on les regroupe :

* « fixes » : distincts à translation près (orientation et sens comptent) ;
* « libres » : distincts à rotation, symétrie et translation près, c'est-à-dire
  les vraies formes différentes de circuits.

Nombres de polygones fixes pour n = 4, 6, 8, 10, 12, 14 : 1, 2, 7, 28, 124, 588.
"""

from __future__ import annotations

from .geometrie import DELTAS

Sommet = tuple[int, int]


def _cycles_depuis_origine(n: int):
    """Tous les cycles simples de n arêtes passant par (0, 0), en listes de sommets."""
    chemin = [(0, 0)]
    vus = {(0, 0)}

    def explorer():
        x, y = chemin[-1]
        restant = n - (len(chemin) - 1)
        if restant == 0:
            if (x, y) == (0, 0):
                yield list(chemin)
            return
        for dx, dy in DELTAS:
            q = (x + dx, y + dy)
            if abs(q[0]) + abs(q[1]) > restant - 1:
                continue                      # trop loin pour revenir à temps
            if q == (0, 0) and restant == 1:
                chemin.append(q)
                yield list(chemin)
                chemin.pop()
            elif q not in vus and q != (0, 0):
                vus.add(q)
                chemin.append(q)
                yield from explorer()
                chemin.pop()
                vus.discard(q)

    yield from explorer()


def _aretes(sommets) -> frozenset:
    return frozenset(frozenset((p, q)) for p, q in zip(sommets, sommets[1:]))


def _normaliser(aretes) -> frozenset:
    """Translate pour que le plus petit x et le plus petit y valent 0."""
    xs = [p[0] for a in aretes for p in a]
    ys = [p[1] for a in aretes for p in a]
    mx, my = min(xs), min(ys)
    return frozenset(frozenset((p[0] - mx, p[1] - my) for p in a) for a in aretes)


_SYMETRIES = [
    lambda x, y: (x, y), lambda x, y: (-y, x), lambda x, y: (-x, -y), lambda x, y: (y, -x),
    lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (y, x), lambda x, y: (-y, -x),
]


def _cle(aretes) -> tuple:
    return tuple(sorted(tuple(sorted(a)) for a in aretes))


def _forme_libre(aretes) -> tuple:
    """Représentant canonique d'un polygone à rotation, symétrie et translation près."""
    meilleure = None
    for s in _SYMETRIES:
        image = _normaliser(frozenset(frozenset(s(*p) for p in a) for a in aretes))
        cle = _cle(image)
        if meilleure is None or cle < meilleure:
            meilleure = cle
    return meilleure


def _tourne_vers_nord(sommets) -> list[Sommet]:
    """Réécrit le cycle (éventuellement à l'envers) pour démarrer sur une arête
    orientée vers le nord : tout polygone en possède une dans l'un des deux sens."""
    for cycle in (sommets[:-1], sommets[:-1][::-1]):
        n = len(cycle)
        for i in range(n):
            p, q = cycle[i], cycle[(i + 1) % n]
            if (q[0] - p[0], q[1] - p[1]) == (0, 1):
                ordre = [cycle[(i + k) % n] for k in range(n)]
                return ordre + [ordre[0]]
    raise ValueError("cycle sans arête vers le nord")


def _reconstruire(dirs) -> list[str]:
    """Version claire de la construction : A pour chaque arête, virage entre deux."""
    mot, cap = [], 0
    for k, d in enumerate(dirs):
        if k > 0:
            mot.extend(_virage((d - cap) % 4))
        mot.append("A")
        cap = d
    mot.extend(_virage((0 - cap) % 4))
    return mot


def _virage(reste: int) -> list[str]:
    return [[], ["D"], ["G", "G"], ["G"]][reste]


def polygones_fixes(n: int) -> list[frozenset]:
    """Tous les polygones à n arêtes, à translation près."""
    if n < 4 or n % 2:
        return []
    vus = {}
    for cycle in _cycles_depuis_origine(n):
        a = _normaliser(_aretes(cycle))
        vus.setdefault(a, cycle)
    return list(vus.values())


def nombre_polygones_fixes(n: int) -> int:
    return len(polygones_fixes(n))


def circuits(n: int) -> list[list[str]]:
    """Un circuit (mot A/G/D convenable) par forme libre de n lignes droites."""
    formes: dict[tuple, list[Sommet]] = {}
    for cycle in polygones_fixes(n):
        formes.setdefault(_forme_libre(_aretes(cycle)), cycle)
    resultat = []
    for cycle in formes.values():
        sommets = _tourne_vers_nord(cycle)
        dirs = [DELTAS.index((q[0] - p[0], q[1] - p[1]))
                for p, q in zip(sommets, sommets[1:])]
        resultat.append(_reconstruire(dirs))
    resultat.sort(key=lambda m: (m.count("G") + m.count("D"), "".join(m)))
    return resultat


def circuit_depuis_cases(cases) -> list[str]:
    """Circuit convenable qui longe le contour d'un assemblage de cases carrées
    (un polyomino) : `[(0, 0), (1, 0), (0, 1)]` donne un « L ».

    ValueError si l'assemblage est vide, non connexe, troué ou pincé (contour
    qui se touche en un point : ce ne serait pas un circuit convenable)."""
    cases = set(map(tuple, cases))
    if not cases:
        raise ValueError("aucune case")
    aretes: dict[frozenset, int] = {}
    for x, y in cases:
        coins = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        for a, b in zip(coins, coins[1:] + coins[:1]):
            k = frozenset((a, b))
            aretes[k] = aretes.get(k, 0) + 1
    contour = [k for k, v in aretes.items() if v == 1]
    voisins: dict[Sommet, list[Sommet]] = {}
    for k in contour:
        a, b = tuple(k)
        voisins.setdefault(a, []).append(b)
        voisins.setdefault(b, []).append(a)
    if any(len(v) != 2 for v in voisins.values()):
        raise ValueError("contour pincé ou assemblage non simplement connexe")
    depart = min(voisins)
    cycle, precedent, courant = [depart], None, depart
    while True:
        suivant = next(q for q in voisins[courant] if q != precedent)
        cycle.append(suivant)
        precedent, courant = courant, suivant
        if courant == depart:
            break
    if len(cycle) - 1 != len(contour):
        raise ValueError("assemblage non connexe (plusieurs contours)")
    sommets = _tourne_vers_nord(cycle)
    dirs = [DELTAS.index((q[0] - p[0], q[1] - p[1])) for p, q in zip(sommets, sommets[1:])]
    return _reconstruire(dirs)
