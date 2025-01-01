AMAX = 10  # accélération maximale en m/s²
FMAX = -20  # freinage maximal en m/s²
VMAX = 100  # vitesse maximale en m/s

def vr(r:int) -> float:
    # Exemple de calcul de la vitesse recommandée pour un virage de rayon r
    return min(VMAX, 10 * r**0.5)

def vitesses_entrée_max(c:list, vf:float) -> [float]:
    n = len(c)
    vitesses = [0] * (n + 1)
    vitesses[-1] = vf

    for i in range(n - 1, -1, -1):
        if c[i][0] == "V":  # Virage
            r = c[i][1]
            vitesses[i] = min(vitesses[i + 1], vr(r))
        else:  # Ligne droite
            d = c[i][1]
            v2 = vitesses[i + 1]
            v1 = (v2**2 + 2 * FMAX * d)**0.5 if v2**2 + 2 * FMAX * d >= 0 else 0
            vitesses[i] = min(vitesses[i + 1], v1)
    
    return vitesses[:-1]

def temps_droite(d:int, v1:float, v2:float) -> (float, float):
    if v1 < v2:
        t1 = (v2 - v1) / AMAX
        d1 = (v1 * t1) + (0.5 * AMAX * t1**2)
        if d1 > d:
            raise ValueError("Impossible de sortir de la ligne droite avec une vitesse inférieure ou égale à v2")
        t = t1 + (d - d1) / v2
        return t, v2
    else:
        t2 = (v1 - v2) / abs(FMAX)
        d2 = (v1 * t2) - (0.5 * abs(FMAX) * t2**2)
        if d2 > d:
            raise ValueError("Impossible de sortir de la ligne droite avec une vitesse inférieure ou égale à v2")
        t = t2 + (d - d2) / v2
        return t, v2

def temps_tour(c:list, v0:float, vf:float) -> float:
    vitesses_max = vitesses_entrée_max(c, vf)
    temps_total = 0
    v = v0

    for i, segment in enumerate(c):
        if segment[0] == "V":
            r = segment[1]
            v = min(vitesses_max[i], vr(r))
        else:
            d = segment[1]
            t, v = temps_droite(d, v, vitesses_max[i + 1])
            temps_total += t
    
    return temps_total

def temps_course(c:list, n:int) -> float:
    """
    Calcule le temps minimal nécessaire pour effectuer une course de n tours du circuit c.
    
    Paramètres:
    c (list): Représentation du circuit (liste de segments).
    n (int): Nombre de tours de circuit.
    
    Retourne:
    float: Temps minimal nécessaire en secondes.
    """
    # Calculer le temps pour un tour en partant de l'arrêt et en terminant avec vf = VMAX
    temps_premier_tour = temps_tour(c, 0, VMAX)
    
    # Calculer le temps pour un tour en tenant compte de la vitesse d'entrée du tour précédent
    vitesses = vitesses_entrée_max(c, VMAX)
    temps_tours_suivants = temps_tour(c, vitesses[0], VMAX)
    
    # Calculer le temps total en ajoutant le temps du premier tour et les temps des tours suivants
    temps_total = temps_premier_tour + (n - 1) * temps_tours_suivants
    return temps_total

# Exemple de test
circuit = [("D", 100), ("V", 50), ("D", 200), ("V", 30)]
n = 5
print(temps_course(circuit, n))