"""Dessin d'un circuit A/G/D : export SVG (sans dépendance) ou turtle."""

from __future__ import annotations

from .geometrie import trajectoire, valider


def circuit_en_svg(c, d: float = 40, marge: float = 30) -> str:
    """Retourne le circuit sous forme de document SVG."""
    pts = trajectoire(c)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    largeur = (max(xs) - min(xs)) * d + 2 * marge
    hauteur = (max(ys) - min(ys)) * d + 2 * marge

    def conv(p):  # axe y vers le haut
        return (marge + (p[0] - min(xs)) * d, marge + (max(ys) - p[1]) * d)

    chemin = " ".join(f"{x:.1f},{y:.1f}" for x, y in map(conv, pts))
    x0, y0 = conv(pts[0])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur:.0f}" '
        f'height="{hauteur:.0f}" viewBox="0 0 {largeur:.0f} {hauteur:.0f}">'
        f'<rect width="100%" height="100%" fill="white"/>'
        f'<polyline points="{chemin}" fill="none" stroke="#222" stroke-width="6" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="7" fill="#d62828"/></svg>'
    )


def dessine_circuit(c, d: float = 50, vitesse: int = 0, attendre: bool = True) -> None:
    """Dessine le circuit avec turtle (cap initial au nord)."""
    import turtle

    turtle.reset()
    turtle.speed(vitesse)
    turtle.setheading(90)
    for e in valider(c):
        if e == "A":
            turtle.forward(d)
        elif e == "G":
            turtle.left(90)
        else:
            turtle.right(90)
    if attendre:
        turtle.done()
