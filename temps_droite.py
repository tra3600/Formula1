def temps_droite(d, v1, v2):
    """
    Calcule le temps minimal nécessaire pour parcourir une ligne droite et la vitesse atteinte.
    
    Paramètres:
    d (int): Longueur de la ligne droite en mètres.
    v1 (float): Vitesse à l'entrée de la ligne droite en m/s.
    v2 (float): Vitesse à la sortie de la ligne droite en m/s.
    
    Retourne:
    tuple: Temps minimal nécessaire et vitesse effectivement atteinte (en secondes et m/s).
    """
    AMAX = 10 # accélération maximale en m/s²
    FMAX = -20 # freinage maximal en m/s²
    VMAX = 100 # vitesse maximale en m/s

    if v1 < v2:
        # Accélération
        t1 = (v2 - v1) / AMAX
        d1 = (v1 * t1) + (0.5 * AMAX * t1**2)
        if d1 > d:
            raise ValueError("Impossible de sortir de la ligne droite avec une vitesse inférieure ou égale à v2")
        t = t1 + (d - d1) / v2
        return t, v2
    else:
        # Décélération
        t2 = (v1 - v2) / abs(FMAX)
        d2 = (v1 * t2) - (0.5 * abs(FMAX) * t2**2)
        if d2 > d:
            raise ValueError("Impossible de sortir de la ligne droite avec une vitesse inférieure ou égale à v2")
        t = t2 + (d - d2) / v2
        return t, v2

# Exemple de test
d = 100
v1 = 20
v2 = 50
print(temps_droite(d, v1, v2))