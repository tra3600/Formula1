def contient_demi_tour1(c):
    """
    Vérifie si le circuit contient un demi-tour.
    
    Paramètres:
    c (list of str): Liste représentant le circuit, contenant "A", "G" et "D".
    
    Retourne:
    bool: True si le circuit contient un demi-tour, False sinon.
    """
    for i in range(len(c) - 1):
        # Vérifie si deux virages consécutifs dans la même direction existent
        if (c[i] == "G" and c[i + 1] == "G") or (c[i] == "D" and c[i + 1] == "D"):
            return True
    return False

# Exemples de tests
print(contient_demi_tour1(["A", "G", "A", "G", "A", "D", "A", "G", "A", "G", "A", "A", "G", "A"]))  # False
print(contient_demi_tour1(["A", "G", "G", "A", "D", "D", "A", "G", "A"]))  # True
print(contient_demi_tour1(["A", "G", "A", "D", "A", "G", "A"]))  # False