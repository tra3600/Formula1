def temps_tour(c, v0, vf):
    """
    Calcule le temps minimal pour effectuer un tour de circuit.
    
    Paramètres:
    c (list): Représentation du circuit (liste de segments).
    v0 (float): Vitesse à l'entrée du circuit en m/s.
    vf (float): Vitesse maximale autorisée à la fin du tour en m/s.
    
    Retourne:
    float: Temps minimal pour effectuer un tour de circuit en secondes.
    """
    vitesses_max = vitesses_entrée_max(c, vf)
    temps_total = 0
    v = v0

    for i, segment in enumerate(c):
        if segment[0] == "V":
            r = segment[1]
            v = min(vitesses_max[i], vr(r))
            # On suppose que le temps passé dans un virage est négligeable pour simplifier
        else:
            d = segment[1]
            t, v = temps_droite(d, v, vitesses_max[i + 1])
            temps_total += t
    
    return temps_total

# Exemple de test
circuit = [("D", 100), ("V", 50), ("D", 200), ("V", 30)]
v0 = 0
vf = 50
print(temps_tour(circuit, v0, vf))