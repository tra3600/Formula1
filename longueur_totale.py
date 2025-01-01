import math
import numpy as np
import turtle

def longueur1(c, d):
    """
    Calcule la longueur totale d'un circuit.
    
    Paramètres:
    c (list of str): Liste représentant le circuit, contenant "A", "G" et "D".
    d (int): Longueur en mètres des portions de ligne droite.
    
    Retourne:
    int: Longueur totale du circuit en mètres.
    """
    # Compter le nombre de segments de droite dans la liste
    nb_lignes_droites = c.count("A")
    
    # La longueur totale est le nombre de segments de droite multiplié par la longueur d'un segment
    longueur_totale = nb_lignes_droites * d
    
    return longueur_totale

# Exemple de test
circuit = ["A", "G", "A", "G", "A", "D", "A", "G", "A", "G", "A", "A", "G", "A"]
longueur_segment = 100  # par exemple, chaque segment de ligne droite fait 100 mètres
print(longueur1(circuit, longueur_segment))  # Affiche 800