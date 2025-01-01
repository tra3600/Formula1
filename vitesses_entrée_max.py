def vr(r):
    # Exemple de calcul de la vitesse recommandée pour un virage de rayon r
    return min(VMAX, 10 * r**0.5)

def vitesses_entrée_max(c, vf):
    """
    Calcule la vitesse maximale à l'entrée de chaque élément du circuit.
    
    Paramètres:
    c (list): Représentation du circuit (liste de segments).
    vf (float): Vitesse maximale à respecter à la fin du circuit.
    
    Retourne:
    list: Vitesse maximale à l'entrée de chaque élément du circuit.
    """
    FMAX = -20 # freinage maximal en m/s²
    VMAX = 100 # vitesse maximale en m/s
    
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

# Exemple de test
circuit = [("V", 50), ("D", 100), ("V", 30), ("D", 200)]
vf = 50
print(vitesses_entrée_max(circuit, vf))