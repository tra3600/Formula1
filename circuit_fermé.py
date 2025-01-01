def est_fermé1(c):
    """
    Détermine si le circuit est fermé.
    
    Paramètres:
    c (list of str): Liste représentant le circuit, contenant "A", "G" et "D".
    
    Retourne:
    bool: True si le circuit est fermé, False sinon.
    """
    # Position initiale et direction
    x, y = 0, 0
    direction = 0  # 0: Nord, 1: Est, 2: Sud, 3: Ouest
    
    # Deltas pour les mouvements dans les directions Nord, Est, Sud, Ouest
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for e in c:
        if e == "A":
            dx, dy = deltas[direction]
            x += dx
            y += dy
        elif e == "G":
            direction = (direction - 1) % 4
        elif e == "D":
            direction = (direction + 1) % 4
    
    # Le circuit est fermé si la position finale est (0, 0) et la direction est Nord (0)
    return (x, y) == (0, 0) and direction == 0

# Exemples de tests
circuit1 = ["A", "G", "A", "G", "A", "G", "A", "G"]
circuit2 = ["A", "A", "G", "A", "A", "G", "A", "A", "G", "A", "A", "G"]
circuit3 = ["A", "G", "A", "D", "A", "D", "A", "G"]

print(est_fermé1(circuit1))  # True, circuit fermé
print(est_fermé1(circuit2))  # False, circuit non fermé
print(est_fermé1(circuit3))  # True, circuit fermé