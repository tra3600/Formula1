import turtle

def dessine_circuit1(c, d):
    """
    Dessine un circuit à l'aide de la bibliothèque turtle.
    
    Paramètres:
    c (list of str): Liste représentant le circuit, contenant "A", "G" et "D".
    d (int): Longueur en pixels des portions de ligne droite.
    """
    # Initialisation de la fenêtre et de la tortue
    turtle.reset()
    turtle.speed(1)  # Vitesse de la tortue (1 est la plus lente, 10 est rapide)
    
    for e in c:
        if e == "A":
            turtle.forward(d)
        elif e == "G":
            turtle.left(90)
        elif e == "D":
            turtle.right(90)

    # Garder la fenêtre ouverte jusqu'à ce qu'elle soit fermée par l'utilisateur
    turtle.done()

# Exemple de test
circuit = ["A", "G", "A", "G", "A", "D", "A", "G", "A", "G", "A", "A", "G", "A"]
longueur_segment = 50  # Longueur en pixels de chaque segment de ligne droite
dessine_circuit1(circuit, longueur_segment)