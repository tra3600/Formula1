def est_fermé1(c):
    """
    Détermine si le circuit est fermé.
    
    Paramètres:
    c (list of str): Liste représentant le circuit, contenant "A", "G" et "D".
    
    Retourne:
    bool: True si le circuit est fermé, False sinon.
    """
    x, y = 0, 0
    direction = 0  # 0: Nord, 1: Est, 2: Sud, 3: Ouest
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

    return (x, y) == (0, 0) and direction == 0

def contient_demi_tour1(c):
    """
    Vérifie si le circuit contient un demi-tour.
    
    Paramètres:
    c (list of str): Liste représentant le circuit, contenant "A", "G" et "D".
    
    Retourne:
    bool: True si le circuit contient un demi-tour, False sinon.
    """
    for i in range(len(c) - 1):
        if (c[i] == "G" and c[i + 1] == "G") or (c[i] == "D" and c[i + 1] == "D"):
            return True
    return False

def circuit_convenable1(c):
    """
    Détermine si le circuit est convenable.
    
    Paramètres:
    c (list of str): Liste représentant le circuit, contenant "A", "G" et "D".
    
    Retourne:
    bool: True si le circuit est fermé, ne contient pas de demi-tour et n'a pas de sections qui se superposent ou se croisent, False sinon.
    """
    if not est_fermé1(c):
        return False

    if contient_demi_tour1(c):
        return False

    x, y = 0, 0
    direction = 0  # 0: Nord, 1: Est, 2: Sud, 3: Ouest
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited_positions = set()
    visited_positions.add((x, y))

    for e in c:
        if e == "A":
            dx, dy = deltas[direction]
            x += dx
            y += dy
            if (x, y) in visited_positions:
                return False
            visited_positions.add((x, y))
        elif e == "G":
            direction = (direction - 1) % 4
        elif e == "D":
            direction = (direction + 1) % 4

    return True

# Exemples de tests
circuit1 = ["A", "G", "A", "G", "A", "G", "A", "G"]  # Circuit fermé sans demi-tour ni croisement
circuit2 = ["A", "A", "G", "A", "A", "G", "A", "A", "G", "A", "A", "G"]  # Circuit non fermé
circuit3 = ["A", "G", "A", "D", "A", "D", "A", "G"]  # Circuit fermé sans demi-tour mais avec croisement

print(circuit_convenable1(circuit1))  # True
print(circuit_convenable1(circuit2))  # False
print(circuit_convenable1(circuit3))  # False