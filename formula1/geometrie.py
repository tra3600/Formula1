"""Circuits à angles droits : listes de "A" (avancer), "G" (gauche), "D" (droite)."""

from __future__ import annotations

# Nord, Est, Sud, Ouest
DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def valider(c) -> list[str]:
    """Vérifie que le circuit ne contient que "A", "G" et "D"."""
    c = list(c)
    for e in c:
        if e not in ("A", "G", "D"):
            raise ValueError(f"élément de circuit invalide : {e!r} (attendu A, G ou D)")
    return c


def _par_element(x, n: int, nom: str) -> list[float]:
    """Un nombre (valable pour tous) ou une suite de n nombres (un par élément)."""
    if isinstance(x, (int, float)):
        return [float(x)] * n
    x = [float(v) for v in x]
    if len(x) != n:
        raise ValueError(f"{nom} : {n} valeurs attendues, {len(x)} reçues")
    return x


def longueur(c, d) -> float:
    """Longueur totale : somme des longueurs des "A". `d` est soit un nombre
    (toutes les lignes droites identiques), soit une suite (un "A" chacun)."""
    c = valider(c)
    return sum(_par_element(d, c.count("A"), "d"))


def trajectoire(c) -> list[tuple[int, int]]:
    """Points de la grille parcourus (départ en (0, 0), cap au nord)."""
    x = y = direction = 0
    points = [(0, 0)]
    for e in valider(c):
        if e == "A":
            dx, dy = DELTAS[direction]
            x, y = x + dx, y + dy
            points.append((x, y))
        elif e == "G":
            direction = (direction - 1) % 4
        else:
            direction = (direction + 1) % 4
    return points


def _cap_final(c) -> int:
    return sum(1 if e == "D" else -1 for e in c if e != "A") % 4


def est_ferme(c) -> bool:
    """Vrai si la voiture revient au départ avec le même cap."""
    c = valider(c)
    return trajectoire(c)[-1] == (0, 0) and _cap_final(c) == 0


def _virages_nets(c) -> list[int]:
    """Rotation nette (mod 4, en quarts de tour à droite) entre deux "A" consécutifs,
    en considérant le circuit comme cyclique."""
    if "A" not in c:
        return []
    i = c.index("A")
    c = c[i:] + c[:i]
    groupes, courant = [], 0
    for e in c[1:] + ["A"]:
        if e == "A":
            groupes.append(courant % 4)
            courant = 0
        else:
            courant += 1 if e == "D" else -1
    return groupes


def representation_minimale(c) -> list[str]:
    """Représentation équivalente où chaque suite de virages entre deux lignes
    droites est réduite à "", "G", "GG" ou "D"."""
    virages = [[], ["G"], ["G", "G"], ["D"]]
    nbg = 0
    res: list[str] = []
    for e in valider(c):
        if e == "A":
            res.extend(virages[nbg])
            nbg = 0
            res.append("A")
        elif e == "G":
            nbg = (nbg + 1) % 4
        else:
            nbg = (nbg - 1) % 4
    res.extend(virages[nbg])
    return res


def contient_demi_tour(c) -> bool:
    """Vrai si une suite de virages entre deux lignes droites fait un demi-tour
    (rotation nette de 180°), y compris "GD..." annulés et "GG"/"DD"."""
    c = valider(c)
    if "A" not in c:
        return sum(1 if e == "D" else -1 for e in c) % 4 == 2
    return 2 in _virages_nets(c)


def circuit_convenable(c) -> bool:
    """Fermé, sans demi-tour, sans croisement ni superposition."""
    c = valider(c)
    if "A" not in c or not est_ferme(c) or contient_demi_tour(c):
        return False
    points = trajectoire(c)
    # le dernier point est le retour au départ, seul point autorisé en double
    return len(set(points[:-1])) == len(points) - 1


def depuis_geometrie(c, d, r) -> list[tuple[str, float]]:
    """Convertit un circuit A/G/D en segments cinématiques :
    ("D", longueur) pour les lignes droites (les "A" consécutifs sont fusionnés)
    et ("V", rayon) pour chaque virage.

    `d` (longueur d'un "A") et `r` (rayon d'un virage) sont soit des nombres,
    soit des suites donnant une valeur par "A" / par virage (circuits « à
    géométrie variable »).
    """
    c = valider(c)
    ds = iter(_par_element(d, c.count("A"), "d"))
    rs = iter(_par_element(r, len(c) - c.count("A"), "r"))
    segments: list[tuple[str, float]] = []
    for e in c:
        if e == "A":
            x = next(ds)
            if segments and segments[-1][0] == "D":
                segments[-1] = ("D", segments[-1][1] + x)
            else:
                segments.append(("D", x))
        else:
            segments.append(("V", next(rs)))
    return segments


def carte_segments(c) -> list[int]:
    """Pour chaque lettre du circuit, l'indice du segment cinématique
    correspondant dans `depuis_geometrie(c, ...)` (les "A" consécutifs
    partagent le même segment)."""
    carte, j, precedent = [], -1, None
    for e in valider(c):
        if e != "A" or precedent != "A":
            j += 1
        carte.append(j)
        precedent = e
    return carte


def rotations(c) -> list[list[str]]:
    """Toutes les façons de placer la ligne de départ sur un circuit fermé
    (décalages circulaires du mot ; la forme du circuit ne change pas)."""
    c = valider(c)
    return [c[i:] + c[:i] for i in range(len(c))]


def diagnostic(c) -> list[str]:
    """Liste des raisons pour lesquelles le circuit n'est pas convenable
    (vide si `circuit_convenable(c)`)."""
    c = valider(c)
    raisons = []
    if "A" not in c:
        return ["aucune ligne droite"]
    pts = trajectoire(c)
    if pts[-1] != (0, 0):
        raisons.append(f"non fermé : la voiture s'arrête en {pts[-1]} et non en (0, 0)")
    elif _cap_final(c) != 0:
        raisons.append(f"cap final différent du cap initial ({90 * _cap_final(c)}° à droite)")
    if contient_demi_tour(c):
        raisons.append("demi-tour entre deux lignes droites")
    aretes, vus = set(), set()
    for p, q in zip(pts, pts[1:]):
        arete = frozenset((p, q))
        if arete in aretes:
            raisons.append(f"superposition : l'arête {p}–{q} est parcourue deux fois")
            break
        aretes.add(arete)
    for p in pts[1:-1] if pts[-1] == (0, 0) else pts[1:]:
        if p in vus:
            raisons.append(f"croisement : le point {p} est visité deux fois")
            break
        vus.add(p)
    if pts[-1] != (0, 0) and pts[-1] in pts[:-1]:
        raisons.append(f"croisement : le point {pts[-1]} est visité deux fois")
    return raisons
