# Formula1
Modélisations autour de la Formule 1

Pour répondre à cette question, nous allons écrire une fonction longueur1 qui calcule la longueur totale d'un circuit composé de segments de droite et de virages à angle droit. La fonction prendra en entrée une liste représentant le circuit et la longueur en mètres des portions de ligne droite. La longueur totale du circuit sera simplement la somme des longueurs des segments de droite, puisque les virages n'ajoutent pas de longueur au circuit.

Explications
Importations :

math, numpy et turtle sont importés car mentionnés dans la consigne pour les prochaines questions, même s'ils ne sont pas utilisés dans cette fonction.
Fonction longueur1 :

La fonction prend deux paramètres :
c: une liste de chaînes de caractères représentant le circuit (les valeurs possibles sont "A", "G", et "D").
d: un entier représentant la longueur en mètres des portions de ligne droite.
La fonction compte le nombre d'occurrences de "A" dans la liste c en utilisant la méthode count.
La longueur totale du circuit est alors calculée en multipliant ce nombre par la longueur d.
La fonction retourne la longueur totale du circuit en mètres.
Exemple de test :

Un exemple de circuit est fourni sous forme de liste.
La longueur d'un segment de ligne droite est définie (par exemple, 100 mètres).
La fonction longueur1 est appelée avec ces paramètres et le résultat est affiché.
Conclusion
Cette fonction est simple et efficace pour calculer la longueur totale d'un circuit composé de segments de droite et de virages à angle droit. Elle utilise les méthodes de base de manipulation de listes en Python et respecte les spécifications de l'énoncé.

Q2: Valeur de l'expression représentation_minimale(["A", "A", "G", "D", "G", "G", "G", "A"])
Pour déterminer la valeur de l'expression représentation_minimale(["A", "A", "G", "D", "G", "G", "G", "A"]), nous devons suivre l'exécution de la fonction pas à pas.

Analysons l'exécution de cette fonction avec l'entrée ["A", "A", "G", "D", "G", "G", "G", "A"] :

Initialisation :

virages = [[], ["G"], ["G", "G"], ["D"]]
nbg = 0
res = []
Premier élément ("A") :

res.extend(virages[nbg]) → res.extend([]) → res = []
nbg = 0
res.append("A") → res = ["A"]
res.extend(virages[nbg]) → res.extend([]) → res = ["A"]
Deuxième élément ("A") :

res.extend(virages[nbg]) → res.extend([]) → res = ["A"]
nbg = 0
res.append("A") → res = ["A", "A"]
res.extend(virages[nbg]) → res.extend([]) → res = ["A", "A"]
Troisième élément ("G") :

nbg = (nbg + 1) % 4 → nbg = 1
res.extend(virages[nbg]) → res.extend(["G"]) → res = ["A", "A", "G"]
Quatrième élément ("D") :

nbg = (nbg - 1) % 4 → nbg = 0
res.extend(virages[nbg]) → res.extend([]) → res = ["A", "A", "G"]
Cinquième élément ("G") :

nbg = (nbg + 1) % 4 → nbg = 1
res.extend(virages[nbg]) → res.extend(["G"]) → res = ["A", "A", "G", "G"]
Sixième élément ("G") :

nbg = (nbg + 1) % 4 → nbg = 2
res.extend(virages[nbg]) → res.extend(["G", "G"]) → res = ["A", "A", "G", "G", "G", "G"]
Septième élément ("G") :

nbg = (nbg + 1) % 4 → nbg = 3
res.extend(virages[nbg]) → res.extend(["D"]) → res = ["A", "A", "G", "G", "G", "G", "D"]
Huitième élément ("A") :

res.extend(virages[nbg]) → res.extend(["D"]) → res = ["A", "A", "G", "G", "G", "G", "D", "D"]
nbg = 0
res.append("A") → res = ["A", "A", "G", "G", "G", "G", "D", "D", "A"]
res.extend(virages[nbg]) → res.extend([]) → res = ["A", "A", "G", "G", "G", "G", "D", "D", "A"]
La valeur de l'expression représentation_minimale(["A", "A", "G", "D", "G", "G", "G", "A"]) est donc ["A", "A", "G", "G", "G", "G", "D", "D", "A"].

Q3: Explication du but de la fonction représentation_minimale
La fonction représentation_minimale a pour but de simplifier la représentation d'un circuit en ligne droite et virages à angle droit. Elle prend en entrée une liste de segments de circuit représentés par des chaînes de caractères "A" (ligne droite), "G" (virage à gauche) et "D" (virage à droite).

Étapes de la fonction :
Initialisation :

virages est une liste de listes représentant les séquences de virages à 90° à gauche et à droite.
nbg est un compteur qui garde la trace du nombre de virages successifs.
res est la liste résultante où sera stockée la représentation minimale.
Boucle sur les éléments de la liste c :

Si l'élément est "A" (ligne droite), la fonction ajoute la séquence de virages accumulés à res et réinitialise le compteur nbg à 0 avant d'ajouter "A" à res.
Si l'élément est "G" (virage à gauche), la fonction incrémente nbg de 1 modulo 4.
Si l'élément est "D" (virage à droite), la fonction décrémente nbg de 1 modulo 4.
Après chaque mise à jour de nbg, la fonction ajoute la séquence de virages correspondants à res.
Finalité :
La fonction convertit une séquence de commandes de circuit en une représentation minimale en ajoutant uniquement les virages nécessaires entre les segments de ligne droite. Cela permet de simplifier la représentation et de s'assurer que les virages sont correctement ajoutés au circuit.

Pour déterminer si un circuit contient un demi-tour, nous devons vérifier si la liste de segments de circuit contient deux virages consécutifs dans la même direction (soit deux "G" consécutifs, soit deux "D" consécutifs). Si c'est le cas, le circuit contient un demi-tour, sinon il ne le contient pas.

Explications
Fonction contient_demi_tour1 :

La fonction prend en paramètre une liste c représentant le circuit.
Elle parcourt la liste des segments de circuit à l'aide d'une boucle for, en vérifiant chaque paire d'éléments consécutifs.
Si elle trouve deux virages consécutifs dans la même direction (deux "G" ou deux "D"), elle retourne True.
Si elle ne trouve pas de tels virages consécutifs après avoir parcouru toute la liste, elle retourne False.
Exemples de tests :

Le premier test utilise le circuit donné dans la question précédente. Il ne contient pas de demi-tour, donc la fonction retourne False.
Le deuxième test utilise un circuit avec des demi-tours (deux "G" consécutifs et deux "D" consécutifs), donc la fonction retourne True.
Le troisième test utilise un circuit sans demi-tours, donc la fonction retourne False.

Conclusion
Cette fonction permet de vérifier facilement si un circuit contient un demi-tour en parcourant les segments du circuit et en recherchant des virages consécutifs dans la même direction. Elle respecte les spécifications de l'énoncé et est efficace pour les listes de taille raisonnable.

our déterminer si un circuit est fermé, nous devons vérifier que la voiture revient à son point de départ et dans la même orientation après avoir parcouru tout le circuit.

Approche
Position Initiale:

Considérez que la voiture commence à l'origine (0, 0) sur une grille.
La voiture peut se déplacer vers le nord, l'est, le sud ou l'ouest.
Initialement, la voiture fait face au nord.
Mouvements:

"A" (avancer) change la position de la voiture selon la direction actuelle.
"G" (virage à gauche) change la direction de la voiture.
"D" (virage à droite) change la direction de la voiture.
Vérification:

Après avoir parcouru tout le circuit, vérifiez si la position finale est (0, 0) et si la direction est toujours le nord.
Code
Voici la fonction est_fermé1 en Python pour vérifier si un circuit est fermé:

Explications
Initialisation:

La voiture commence à la position (0, 0) et fait face au nord (direction = 0).
Boucle sur les éléments du circuit:

Pour chaque "A", la voiture avance dans la direction actuelle en utilisant les deltas définis.
Pour chaque "G", la voiture tourne à gauche (direction change de -1 modulo 4).
Pour chaque "D", la voiture tourne à droite (direction change de +1 modulo 4).
Vérification finale:

Après avoir parcouru tout le circuit, la fonction vérifie si la position finale est (0, 0) et si la direction est toujours le nord (0).
Conclusion
Cette fonction permet de vérifier efficacement si un circuit est fermé en simulant les mouvements de la voiture et en vérifiant la position et la direction finales. Elle respecte les spécifications de l'énoncé et utilise des techniques simples de manipulation de coordonnées et de direction.

Pour vérifier si un circuit est convenable, il doit satisfaire les critères suivants :

Être fermé.
Ne pas comporter de demi-tour.
Ne pas avoir de sections qui se superposent ou se croisent.
Nous avons déjà les fonctions est_fermé1 et contient_demi_tour1 pour vérifier les deux premiers critères. Pour le troisième critère (les croisements), nous devons vérifier que la trajectoire de la voiture ne repasse pas par une position déjà visitée.

Étapes de la fonction circuit_convenable1
Vérifier que le circuit est fermé en utilisant la fonction est_fermé1.
Vérifier que le circuit ne contient pas de demi-tour en utilisant la fonction contient_demi_tour1.
Vérifier que la voiture ne repasse pas par une position déjà visitée en maintenant un ensemble des positions visitées et en mettant à jour la position de la voiture à chaque mouvement.

Explications
Fonction est_fermé1 :

Vérifie si le circuit est fermé en suivant la position et la direction de la voiture.
Fonction contient_demi_tour1 :

Vérifie si le circuit contient des demi-tours en cherchant des virages consécutifs dans la même direction.
Fonction circuit_convenable1 :

Vérifie d'abord si le circuit est fermé et ne contient pas de demi-tour.
Utilise un ensemble pour garder une trace des positions visitées.
Parcourt le circuit et met à jour la position de la voiture. Si une position est visitée deux fois, cela signifie qu'il y a un croisement, et la fonction retourne False.
Conclusion
Cette fonction permet de vérifier si un circuit est convenable en respectant les critères de fermeture, absence de demi-tours et absence de croisements. Elle utilise des techniques de suivi de position et de vérification de condition pour s'assurer que le circuit est sûr et conforme aux exigences.

Pour dessiner un circuit en utilisant la bibliothèque turtle, nous allons écrire une fonction dessine_circuit1 qui prend en paramètres une représentation d'un circuit et la longueur des segments de ligne droite en pixels. La fonction utilisera les commandes de la bibliothèque turtle pour tracer le circuit à l'écran.

Fonction dessine_circuit1
Initialisation de la tortue: Nous devons initialiser la tortue et la fenêtre de visualisation.
Parcours de la représentation du circuit: Pour chaque élément de la liste, nous ferons avancer la tortue ou la ferons tourner selon le type de segment.
Dessin du circuit: Utiliser les commandes forward, left, et right pour dessiner le circuit.
Code

Explications
Initialisation de la tortue:

turtle.reset(): Réinitialise la fenêtre et repositionne la tortue au centre.
turtle.speed(1): Définit la vitesse de la tortue (1 est la plus lente, 10 est rapide).
Parcours de la représentation du circuit:

Pour chaque élément de la liste c:
Si l'élément est "A", la tortue avance de d pixels.
Si l'élément est "G", la tortue tourne à gauche de 90 degrés.
Si l'élément est "D", la tortue tourne à droite de 90 degrés.
Dessin du circuit:

Les commandes forward, left, et right sont utilisées pour dessiner le circuit en fonction des segments.
Maintenir la fenêtre ouverte:

turtle.done(): Garde la fenêtre ouverte jusqu'à ce qu'elle soit fermée par l'utilisateur.
Conclusion
Cette fonction permet de dessiner un circuit représenté par une liste de segments en utilisant la bibliothèque turtle. Les segments de ligne droite sont dessinés en faisant avancer la tortue, et les virages sont réalisés en faisant tourner la tortue de 90 degrés à gauche ou à droite. Cette approche est simple et efficace pour visualiser des circuits de course basiques.

Pour déterminer le temps nécessaire pour qu'une voiture atteigne sa vitesse maximale 
v
m
a
x
 en accélérant au maximum 
a
m
a
x
, nous pouvons utiliser la formule de la cinématique pour l'accélération constante. La formule de base est:

v
=
a
⋅
t
où:

v
 est la vitesse finale
a
 est l'accélération
t
 est le temps
Nous devons réorganiser cette formule pour résoudre 
t
:

t
=
v
a
En utilisant les valeurs fournies:

a
m
a
x
=
10
m/s
2
v
m
a
x
=
100
m/s
Nous pouvons substituer ces valeurs dans la formule:

t
=
v
m
a
x
a
m
a
x
=
100
m/s
10
m/s
2
=
10
s
Application numérique
Le temps nécessaire pour qu'une voiture atteigne la vitesse maximale de 100 m/s en accélérant au maximum de 10 m/s² est de 10 secondes.

Conclusion
La formule utilisée ici est une application directe de la cinématique pour un mouvement rectiligne uniformément accéléré. En pratique, cela signifie qu'un pilote, en démarrant à l'arrêt et en maintenant l'accélération maximale de la voiture, atteindra la vitesse maximale de 100 m/s (360 km/h) en 10 secondes.

Q 14. Temps minimal nécessaire pour passer de la vitesse 
v
1
 à la vitesse 
v
2
Pour exprimer le temps minimal nécessaire à une voiture pour passer d'une vitesse 
v
1
 à une vitesse 
v
2
, nous devons distinguer deux cas :

v
1
>
v
2
 : La voiture doit freiner.
v
1
<
v
2
 : La voiture doit accélérer.
Cas 1 : 
v
1
>
v
2
 (freinage)
Lorsqu'une voiture doit passer de 
v
1
 à 
v
2
 en freinant, elle subit une accélération négative (freinage maximal 
f
m
a
x
). Utilisons la formule de la cinématique pour une accélération constante :

v
2
=
v
1
+
f
m
a
x
⋅
t
où 
f
m
a
x
 est négatif. Réarrangeons cette équation pour résoudre 
t
 :

t
=
v
2
−
v
1
f
m
a
x
Cas 2 : 
v
1
<
v
2
 (accélération)
Lorsqu'une voiture doit passer de 
v
1
 à 
v
2
 en accélérant, elle subit une accélération positive (accélération maximale 
a
m
a
x
). Utilisons la formule de la cinématique pour une accélération constante :

v
2
=
v
1
+
a
m
a
x
⋅
t
Réarrangeons cette équation pour résoudre 
t
 :

t
=
v
2
−
v
1
a
m
a
x
Application numérique
Pour 
v
1
=
300
km/h
 et 
v
2
=
120
km/h
, nous devons d'abord convertir ces vitesses en m/s :

v
1
=
300
km/h
×
1000
m
1
km
×
1
h
3600
s
=
83.33
m/s
v
2
=
120
km/h
×
1000
m
1
km
×
1
h
3600
s
=
33.33
m/s
Les valeurs de 
a
m
a
x
 et 
f
m
a
x
 sont :

a
m
a
x
=
10
m/s
2
f
m
a
x
=
−
20
m/s
2
Cas 
v
1
>
v
2
 (freinage)
t
=
v
2
−
v
1
f
m
a
x
=
33.33
m/s
−
83.33
m/s
−
20
m/s
2
=
−
50
−
20
=
2.5
s
Donc, le temps minimal nécessaire pour passer de 300 km/h à 120 km/h en freinant est de 2.5 secondes.

Q 15. Distance minimale nécessaire pour passer de 
v
1
 à 
v
2
>
v
1
Pour montrer que la distance minimale nécessaire à une voiture pour passer de 
v
1
 à 
v
2
 (où 
v
2
>
v
1
) est donnée par la formule :

d
=
v
2
2
−
v
1
2
2
a
m
a
x
nous pouvons utiliser la formule de la cinématique qui relie la distance parcourue à la vitesse initiale, la vitesse finale et l'accélération :

v
2
2
=
v
1
2
+
2
a
m
a
x
d
Réarrangeons cette équation pour résoudre 
d
 :

d
=
v
2
2
−
v
1
2
2
a
m
a
x
Cette formule montre que la distance minimale nécessaire pour passer de 
v
1
 à 
v
2
 est proportionnelle à la différence des carrés des vitesses divisé par deux fois l'accélération maximale.

Conclusion
Temps nécessaire pour changer de vitesse:

Pour 
v
1
>
v
2
, le temps est donné par 
t
=
v
2
−
v
1
f
m
a
x
.
Pour 
v
1
<
v
2
, le temps est donné par 
t
=
v
2
−
v
1
a
m
a
x
.
Distance nécessaire pour changer de vitesse:

Pour passer de 
v
1
 à 
v
2
 (où 
v
2
>
v
1
), la distance est donnée par 
d
=
v
2
2
−
v
1
2
2
a
m
a
x
.


Pour déterminer la distance minimale nécessaire à une voiture qui roule en ligne droite à la vitesse 
v
1
 pour passer à la vitesse 
v
2
 (où 
v
2
<
v
1
), nous devons utiliser les formules de cinématique pour une accélération constante, mais en considérant cette fois un freinage maximal 
f
m
a
x
.

Formule de la distance pour freinage
La formule de la distance parcourue lors d'un changement de vitesse avec une accélération constante est donnée par :

v
2
2
=
v
1
2
+
2
a
d
où :

v
1
 est la vitesse initiale
v
2
 est la vitesse finale
a
 est l'accélération (négative pour le freinage)
d
 est la distance parcourue
Pour le cas du freinage, l'accélération 
a
 est 
f
m
a
x
. Réarrangeons cette formule pour résoudre 
d
 :

d
=
v
2
2
−
v
1
2
2
f
m
a
x
Application numérique
Pour 
v
1
=
300
km/h
 et 
v
2
=
120
km/h
, nous devons d'abord convertir ces vitesses en m/s :

v
1
=
300
km/h
×
1000
m
1
km
×
1
h
3600
s
=
83.33
m/s
v
2
=
120
km/h
×
1000
m
1
km
×
1
h
3600
s
=
33.33
m/s
La valeur de 
f
m
a
x
 est :

f
m
a
x
=
−
20
m/s
2
Substituons ces valeurs dans la formule pour 
d
 :

d
=
(
33.33
m/s
)
2
−
(
83.33
m/s
)
2
2
×
(
−
20
m/s
2
)
Calculons les termes :

v
2
2
=
(
33.33
)
2
=
1110.8889
m
2
/
s
2
v
1
2
=
(
83.33
)
2
=
6944.8889
m
2
/
s
2
d
=
1110.8889
−
6944.8889
−
40
d
=
−
5834
−
40
d
=
145.85
m
Conclusion
La distance minimale nécessaire pour qu'une voiture passe de 300 km/h (83.33 m/s) à 120 km/h (33.33 m/s) en freinant avec une décélération maximale de -20 m/s² est de 145.85 mètres.

Pour répondre à ces questions, nous devons utiliser les relations de cinématique pour le mouvement avec accélération et décélération.

Q 17. Exprimer 
d
m
i
n
Pour exprimer la longueur minimale 
d
m
i
n
 de la ligne droite pour que la vitesse 
v
m
a
x
 soit atteinte, nous devons considérer deux phases :

Accélération depuis 
v
1
 jusqu'à 
v
m
a
x
.
Décélération depuis 
v
m
a
x
 jusqu'à 
v
2
.
Phase d'accélération
Utilisons la formule de la distance parcourue lors d'une accélération :

d
1
=
v
m
a
x
2
−
v
1
2
2
a
m
a
x
où :

v
m
a
x
 est la vitesse maximale.
v
1
 est la vitesse initiale.
a
m
a
x
 est l'accélération maximale.
Phase de décélération
Utilisons la formule de la distance parcourue lors d'une décélération :

d
2
=
v
m
a
x
2
−
v
2
2
2
|
f
m
a
x
|
où :

v
m
a
x
 est la vitesse maximale.
v
2
 est la vitesse finale.
f
m
a
x
 est le freinage maximal (négatif, donc nous utilisons la valeur absolue).
Longueur minimale 
d
m
i
n
La longueur minimale 
d
m
i
n
 est la somme des distances d'accélération et de décélération :

d
m
i
n
=
d
1
+
d
2
=
v
m
a
x
2
−
v
1
2
2
a
m
a
x
+
v
m
a
x
2
−
v
2
2
2
|
f
m
a
x
|
Q 18. Temps minimal nécessaire pour parcourir la ligne droite lorsque 
d
≥
d
m
i
n
Si la longueur de la ligne droite est supérieure ou égale à 
d
m
i
n
, la voiture atteindra 
v
m
a
x
 et maintiendra cette vitesse sur une partie de la ligne droite avant de freiner pour atteindre 
v
2
. Nous devons considérer trois phases :

Accélération de 
v
1
 à 
v
m
a
x
.
Parcours à vitesse constante 
v
m
a
x
.
Décélération de 
v
m
a
x
 à 
v
2
.
Temps d'accélération
Le temps pour accélérer de 
v
1
 à 
v
m
a
x
 est donné par :

t
1
=
v
m
a
x
−
v
1
a
m
a
x
Temps de décélération
Le temps pour décélérer de 
v
m
a
x
 à 
v
2
 est donné par :

t
2
=
v
m
a
x
−
v
2
|
f
m
a
x
|
Distance parcourue pendant l'accélération et la décélération
Les distances parcourues pendant l'accélération et la décélération sont 
d
1
 et 
d
2
 respectivement, comme calculé précédemment.

Distance restante à parcourir à vitesse constante
La distance restante 
d
3
 à parcourir à vitesse constante 
v
m
a
x
 est :

d
3
=
d
−
d
1
−
d
2
Temps pour parcourir la distance restante à vitesse constante
Le temps pour parcourir 
d
3
 à vitesse constante 
v
m
a
x
 est :

t
3
=
d
3
v
m
a
x
=
d
−
d
1
−
d
2
v
m
a
x
Temps total
Le temps total 
t
 est la somme des temps des trois phases :

t
=
t
1
+
t
2
+
t
3
=
v
m
a
x
−
v
1
a
m
a
x
+
v
m
a
x
−
v
2
|
f
m
a
x
|
+
d
−
d
1
−
d
2
v
m
a
x
Conclusion
Longueur minimale 
d
m
i
n
 :
d
m
i
n
=
v
m
a
x
2
−
v
1
2
2
a
m
a
x
+
v
m
a
x
2
−
v
2
2
2
|
f
m
a
x
|
Temps minimal 
t
 pour 
d
≥
d
m
i
n
 :
t
=
v
m
a
x
−
v
1
a
m
a
x
+
v
m
a
x
−
v
2
|
f
m
a
x
|
+
d
−
d
1
−
d
2

Pour exprimer le temps minimal nécessaire pour traverser une ligne droite de longueur 
d
 entre deux virages, avec des vitesses de sortie et d'entrée des virages respectivement 
v
1
 et 
v
2
, nous devons considérer deux cas :

d
≥
d
m
i
n
 : La voiture atteindra la vitesse maximale 
v
m
a
x
.
d
<
d
m
i
n
 : La voiture atteindra une vitesse maximale intermédiaire 
v
3
.
Nous avons déjà traité le cas où 
d
≥
d
m
i
n
. Maintenant, nous nous concentrons sur le cas 
d
<
d
m
i
n
 et exprimons le temps minimal nécessaire pour traverser la ligne droite.

Cas 
d
<
d
m
i
n
Dans ce cas, la voiture n'atteint pas la vitesse maximale 
v
m
a
x
. La voiture accélère à partir de 
v
1
 pour atteindre une vitesse maximale intermédiaire 
v
3
 avant de décélérer pour atteindre 
v
2
.

Phase d'accélération
La vitesse maximale atteinte 
v
3
 est atteinte après une certaine distance 
d
1
 et un certain temps 
t
1
. Utilisons les formules de la cinématique pour accélération constante :

v
3
=
v
1
+
a
m
a
x
⋅
t
1
d
1
=
v
3
2
−
v
1
2
2
a
m
a
x
Phase de décélération
La vitesse maximale 
v
3
 est décélérée pour atteindre 
v
2
 sur une distance 
d
2
 et un certain temps 
t
2
. Utilisons les formules de la cinématique pour décélération constante :

v
2
=
v
3
+
f
m
a
x
⋅
t
2
d
2
=
v
3
2
−
v
2
2
2
|
f
m
a
x
|
Temps total
Le temps total 
t
 pour parcourir la distance 
d
 est la somme des temps d'accélération et de décélération :

t
=
t
1
+
t
2
Nous avons les expressions pour 
t
1
 et 
t
2
 :

t
1
=
v
3
−
v
1
a
m
a
x
t
2
=
v
3
−
v
2
|
f
m
a
x
|
Conclusion
Le temps minimal nécessaire pour traverser une ligne droite de longueur 
d
 lorsque 
d
<
d
m
i
n
 est donné par :

t
=
v
3
−
v
1
a
m
a
x
+
v
3
−
v
2
|
f
m
a
x
|
où 
v
3
 est la vitesse maximale atteinte dans la ligne droite. Notez que 
v
3
 dépend de la distance 
d
 et doit être calculée en conséquence.

 Q 20. Fonction vitesses_entrée_max
La fonction vitesses_entrée_max calcule la vitesse maximale à l'entrée de chaque élément du circuit pour ne jamais dépasser la vitesse recommandée dans les virages suivants ni la vitesse finale maximale 
v
f
. Nous devons parcourir le circuit à l'envers pour tenir compte des contraintes des virages suivants.

Q 21. Fonction temps_droite
La fonction temps_droite calcule le temps minimal nécessaire pour parcourir une ligne droite de longueur 
d
 en entrant à la vitesse 
v
1
 et en sortant à la vitesse 
v
2
. Si ce n'est pas possible, elle lève une exception ValueError.

Q 22. Fonction temps_tour
La fonction temps_tour calcule le temps minimal pour effectuer un tour de circuit en tenant compte des vitesses maximales aux entrées de chaque élément du circuit.

Explications
Fonction vitesses_entrée_max :

Parcourt le circuit à l'envers pour déterminer les vitesses maximales à l'entrée de chaque segment.
Utilise la vitesse recommandée pour les virages et les formules de cinématique pour les lignes droites.
Fonction temps_droite :

Calcule le temps minimal pour parcourir une ligne droite en fonction de la longueur et des vitesses d'entrée et de sortie.
Utilise les formules de cinématique pour l'accélération et le freinage.
Fonction temps_tour :

Utilise vitesses_entrée_max pour obtenir les vitesses maximales aux entrées des segments.
Calcule le temps minimal pour parcourir chaque segment et accumule le temps total.
Ces fonctions permettent de simuler le parcours d'un circuit en tenant compte des contraintes de vitesse et des caractéristiques des segments.

Pour calculer le temps minimal nécessaire pour effectuer une course de 
n
 tours du circuit 
c
, nous devons considérer que :

La voiture démarre à l'arrêt au début de la course.
La vitesse doit être contrôlée pour chaque virage et ligne droite selon les contraintes de vitesse maximale.
À la fin du dernier tour, la vitesse n'est pas limitée.
Nous allons utiliser les fonctions précédemment définies (vitesses_entrée_max, temps_droite, et temps_tour) pour calculer le temps pour chaque tour et ensuite multiplier par le nombre de tours 
n
.

Q 24. Complexité temporelle asymptotique
Analysons la complexité temporelle asymptotique dans le pire des cas de la fonction temps_course en fonction de 
n
 et du nombre de segments du circuit 
c
 (longueur de la liste).

Fonction vitesses_entrée_max:

Cette fonction parcourt la liste des segments du circuit une fois, donc sa complexité est 
O
(
m
)
, où 
m
 est le nombre de segments du circuit.
Fonction temps_droite:

Cette fonction a une complexité constante 
O
(
1
)
 car elle effectue un nombre fixe de calculs.
Fonction temps_tour:

Cette fonction parcourt la liste des segments du circuit une fois et appelle temps_droite pour chaque segment, donc sa complexité est 
O
(
m
)
.
Fonction temps_course:

Cette fonction appelle temps_tour une fois pour le premier tour et une fois pour les tours suivants, donc sa complexité est 
O
(
m
)
 pour le premier tour et 
O
(
m
)
 pour chaque tour suivant.
Le nombre total de tours est 
n
, donc la complexité totale est 
O
(
n
⋅
m
)
.
Conclusion
La complexité temporelle asymptotique dans le pire des cas de la fonction temps_course est 
O
(
n
⋅
m
)
, où 
n
 est le nombre de tours et 
m
 est le nombre de segments du circuit.
