"""Dessin d'un circuit A/G/D : export SVG (sans dépendance) ou turtle."""

from __future__ import annotations

import math

from .geometrie import DELTAS, _par_element, carte_segments, depuis_geometrie, est_ferme, trajectoire, valider


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


# ----------------------------------------------------------------------
# Circuit coloré selon la vitesse
# ----------------------------------------------------------------------
def couleur_vitesse(v: float, vmax: float) -> str:
    """Bleu (arrêt) → cyan → vert → jaune → rouge (vitesse maximale)."""
    t = 0.0 if vmax <= 0 else max(0.0, min(1.0, v / vmax))
    return f"hsl({240 * (1 - t):.0f},85%,48%)"


def _interpoler(echantillons, x: float) -> float:
    """Vitesse en position x, par interpolation linéaire de (position, vitesse)."""
    if len(echantillons) == 1 or x <= echantillons[0][0]:
        return echantillons[0][1]
    for (x0, v0), (x1, v1) in zip(echantillons, echantillons[1:]):
        if x <= x1:
            return v0 if x1 == x0 else v0 + (v1 - v0) * (x - x0) / (x1 - x0)
    return echantillons[-1][1]


def circuit_vitesse_svg(c, d=200, r=30, params=None, v0=None, vf=None,
                        u: float = 80, marge: float = 40, titre: str | None = None) -> str:
    """Circuit aux coins arrondis, chaque tronçon coloré par la vitesse de la
    voiture lors d'un tour en régime établi (ou entre `v0` et `vf` si donnés).

    `d` et `r` peuvent être des suites (géométrie variable) ; le dessin reste à
    l'échelle d'une grille de pas `u` pixels, quelles que soient les longueurs."""
    from .cinematique import PAR, vitesse_de_ligne
    from .profil import vitesses_sur_segments

    p = params or PAR
    c = valider(c)
    seg = depuis_geometrie(c, d, r)
    s = vitesse_de_ligne(seg, p) if v0 is None else v0
    vit = vitesses_sur_segments(seg, s, s if vf is None else vf, p)
    carte = carte_segments(c)
    longueurs = _par_element(d, c.count("A"), "d")

    aretes, dans_seg = [], {}
    x = y = cap = k = 0
    for i, e in enumerate(c):
        if e == "A":
            dx, dy = DELTAS[cap]
            j = carte[i]
            debut = dans_seg.get(j, 0.0)
            dans_seg[j] = debut + longueurs[k]
            aretes.append({"i": i, "cap": cap, "p0": (x, y), "p1": (x + dx, y + dy),
                           "seg": j, "debut": debut, "long": longueurs[k]})
            x, y, k = x + dx, y + dy, k + 1
        else:
            cap = (cap + (1 if e == "D" else -1)) % 4
    m = len(aretes)
    if m == 0:
        raise ValueError("circuit sans ligne droite")
    ferme = est_ferme(c)

    def coin(a: int) -> bool:
        """Y a-t-il un virage de 90° à la fin de l'arête a ?"""
        if a == m - 1 and not ferme:
            return False
        return (aretes[(a + 1) % m]["cap"] - aretes[a]["cap"]) % 4 in (1, 3)

    pts = trajectoire(c)
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    entete = 46 if titre else 10
    largeur = max((max(xs) - min(xs)) * u + 2 * marge, 300)
    hauteur = (max(ys) - min(ys)) * u + 2 * marge + entete + 40
    decal = (largeur - (max(xs) - min(xs)) * u) / 2

    def px(q):
        return (decal + (q[0] - min(xs)) * u, marge + entete + (max(ys) - q[1]) * u)

    def sens(cap):                       # direction à l'écran (y vers le bas)
        return DELTAS[cap][0], -DELTAS[cap][1]

    rho, epais = 0.22 * u, 9
    corps = []
    for a, ar in enumerate(aretes):
        (X0, Y0), (X1, Y1) = px(ar["p0"]), px(ar["p1"])
        L = math.hypot(X1 - X0, Y1 - Y0)
        deb = rho if coin(a - 1) else 0.0
        fin = L - (rho if coin(a) else 0.0)
        ux, uy = (X1 - X0) / L, (Y1 - Y0) / L
        for q in range(10):
            f0 = deb + (fin - deb) * q / 10
            f1 = deb + (fin - deb) * (q + 1) / 10
            pos = ar["debut"] + (f0 + f1) / 2 / L * ar["long"]
            corps.append(
                f'<line x1="{X0 + ux * f0:.1f}" y1="{Y0 + uy * f0:.1f}" '
                f'x2="{X0 + ux * f1:.1f}" y2="{Y0 + uy * f1:.1f}" '
                f'stroke="{couleur_vitesse(_interpoler(vit[ar["seg"]], pos), p.vmax)}" '
                f'stroke-width="{epais}"/>')
    for a, ar in enumerate(aretes):
        if not coin(a):
            continue
        suivante = aretes[(a + 1) % m]
        droite = (suivante["cap"] - ar["cap"]) % 4 == 1
        Xv, Yv = px(ar["p1"])
        s0, s1 = sens(ar["cap"]), sens(suivante["cap"])
        A = (Xv - s0[0] * rho, Yv - s0[1] * rho)
        B = (Xv + s1[0] * rho, Yv + s1[1] * rho)
        v = vit[carte[(ar["i"] + 1) % len(c)]][0][1]          # vitesse dans le virage
        corps.append(
            f'<path d="M{A[0]:.1f},{A[1]:.1f} A{rho:.1f},{rho:.1f} 0 0 {1 if droite else 0} '
            f'{B[0]:.1f},{B[1]:.1f}" fill="none" stroke="{couleur_vitesse(v, p.vmax)}" '
            f'stroke-width="{epais}"/>')
    X0, Y0 = px(pts[0])
    ly = hauteur - 24
    degrade = "".join(
        f'<rect x="{marge + q * 4}" y="{ly}" width="4" height="10" '
        f'fill="{couleur_vitesse(p.vmax * q / 50, p.vmax)}"/>' for q in range(51))
    police = 'font-family="sans-serif" fill="#333"'
    texte = (f'<text x="{marge}" y="{ly - 4}" font-size="11" {police}>0 km/h</text>'
             f'<text x="{marge + 204}" y="{ly - 4}" font-size="11" text-anchor="end" {police}>'
             f'{p.vmax * 3.6:.0f} km/h</text>')
    tete = (f'<text x="{largeur / 2:.0f}" y="28" text-anchor="middle" font-size="16" '
            f'font-family="sans-serif" fill="#111">{titre}</text>') if titre else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur:.0f}" '
        f'height="{hauteur:.0f}" viewBox="0 0 {largeur:.0f} {hauteur:.0f}">'
        f'<rect width="100%" height="100%" fill="white"/>{tete}' + "".join(corps) +
        f'<circle cx="{X0:.1f}" cy="{Y0:.1f}" r="7" fill="white" stroke="#111" stroke-width="3"/>'
        + degrade + texte + '</svg>')


# ----------------------------------------------------------------------
# Petits graphiques SVG (sans dépendance)
# ----------------------------------------------------------------------
PALETTE = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b"]


def _graduations(lo: float, hi: float, n: int = 6) -> list[float]:
    if hi <= lo:
        hi = lo + 1
    brut = (hi - lo) / n
    puiss = 10 ** math.floor(math.log10(brut))
    pas = min((k * puiss for k in (1, 2, 2.5, 5, 10) if k * puiss >= brut), default=brut)
    debut = math.ceil(lo / pas - 1e-9) * pas
    return [debut + k * pas for k in range(int((hi - lo) / pas + 1e-9) + 1)]


def graphe_svg(series, titre: str, xlabel: str, ylabel: str,
               largeur: int = 640, hauteur: int = 360, y0: float | None = None) -> str:
    """Courbes (étiquette, [(x, y), ...]) dans un cadre gradué ; SVG autonome."""
    tous = [pt for _, pts in series for pt in pts]
    if not tous:
        raise ValueError("aucune donnée")
    xmin, xmax = min(q[0] for q in tous), max(q[0] for q in tous)
    ymin = y0 if y0 is not None else min(q[1] for q in tous)
    ymax = max(q[1] for q in tous)
    if ymax == ymin:
        ymax = ymin + 1
    if xmax == xmin:
        xmax = xmin + 1
    g, dr, hh, bs = 62, 20, 44, 52
    W, H = largeur - g - dr, hauteur - hh - bs

    def X(v):
        return g + (v - xmin) / (xmax - xmin) * W

    def Y(v):
        return hh + H - (v - ymin) / (ymax - ymin) * H

    police = 'font-family="sans-serif" fill="#333"'
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}"><rect width="100%" height="100%" fill="white"/>',
         f'<text x="{largeur / 2:.0f}" y="26" text-anchor="middle" font-size="16" {police}>{titre}</text>']
    for v in _graduations(xmin, xmax):
        o.append(f'<line x1="{X(v):.1f}" y1="{hh}" x2="{X(v):.1f}" y2="{hh + H}" stroke="#e5e5e5"/>'
                 f'<text x="{X(v):.1f}" y="{hh + H + 16}" text-anchor="middle" font-size="11" {police}>{v:g}</text>')
    for v in _graduations(ymin, ymax):
        o.append(f'<line x1="{g}" y1="{Y(v):.1f}" x2="{g + W}" y2="{Y(v):.1f}" stroke="#e5e5e5"/>'
                 f'<text x="{g - 6}" y="{Y(v) + 4:.1f}" text-anchor="end" font-size="11" {police}>{v:g}</text>')
    o.append(f'<rect x="{g}" y="{hh}" width="{W}" height="{H}" fill="none" stroke="#888"/>')
    o.append(f'<text x="{g + W / 2:.0f}" y="{hauteur - 10}" text-anchor="middle" font-size="12" {police}>{xlabel}</text>')
    o.append(f'<text transform="translate(16,{hh + H / 2:.0f}) rotate(-90)" text-anchor="middle" '
             f'font-size="12" {police}>{ylabel}</text>')
    for k, (nom, pts) in enumerate(series):
        col = PALETTE[k % len(PALETTE)]
        chemin = " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in pts)
        o.append(f'<polyline points="{chemin}" fill="none" stroke="{col}" stroke-width="2.2" '
                 f'stroke-linejoin="round"/>')
        if len(series) > 1 or nom:
            ly = hh + 14 + 16 * k
            o.append(f'<rect x="{g + 10}" y="{ly - 9}" width="14" height="4" fill="{col}"/>'
                     f'<text x="{g + 30}" y="{ly - 3}" font-size="11" {police}>{nom}</text>')
    o.append("</svg>")
    return "".join(o)
