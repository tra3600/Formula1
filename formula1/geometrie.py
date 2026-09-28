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


def longueur(c, d: float) -> float:
    """Longueur totale : nombre de "A" fois la longueur d'une ligne droite."""
    return valider(c).count("A") * d


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


def depuis_geometrie(c, d: float, r: float) -> list[tuple[str, float]]:
    """Convertit un circuit A/G/D en segments cinématiques :
    ("D", longueur) pour les lignes droites (les "A" consécutifs sont fusionnés)
    et ("V", rayon) pour chaque virage."""
    segments: list[tuple[str, float]] = []
    for e in valider(c):
        if e == "A":
            if segments and segments[-1][0] == "D":
                segments[-1] = ("D", segments[-1][1] + d)
            else:
                segments.append(("D", d))
        else:
            segments.append(("V", r))
    return segments
