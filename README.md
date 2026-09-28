# Formula1

Modélisations autour de la Formule 1, d'après le sujet Centrale-Supélec info 2022
(PDF dans `docs/`) : géométrie de circuits à angles droits et calcul du temps de course minimal.

## Utilisation

```bash
python -m formula1 --exemple en_L -n 5 --svg circuit.svg
python -m formula1 ADADADAD -l 200 -r 30 -n 10 --arc
python -m formula1 AAADADAAGADADAAD --turtle
python -m unittest discover -s tests
```

Options : `-l` longueur d'une ligne droite (m), `-r` rayon des virages (m), `-n` tours,
`--amax/--fmax/--vmax`, `--arc` (compte la durée des virages en quart de cercle),
`--svg FICHIER`, `--turtle`. Exemples prédéfinis : `carre`, `rectangle`, `en_L`.
Sans dépendance externe (bibliothèque standard uniquement).

## Modules (`formula1/`)

| Module | Contenu |
|---|---|
| `geometrie` | circuits `A`/`G`/`D` : `longueur`, `representation_minimale`, `est_ferme`, `contient_demi_tour`, `circuit_convenable`, `trajectoire`, `depuis_geometrie` |
| `cinematique` | segments `("D", d)` / `("V", r)` : `vitesses_entree_max`, `temps_droite`, `temps_tour`, `temps_course`, `Parametres` |
| `dessin` | `circuit_en_svg`, `dessine_circuit` (turtle) |
| `cli` | `python -m formula1` |

## Modèle

- Accélération max 10 m/s², freinage max 20 m/s², vitesse max 100 m/s, vitesse en virage `min(vmax, 10·√r)`.
- `temps_droite(d, v1, v2)` : accélération, palier à `vmax` si `d ≥ dmin`, sinon vitesse de pointe intermédiaire `v3` ; `ValueError` si `d` est trop court.
- `temps_course(c, n)` : départ arrêté ; les tours suivants partent à la vitesse de passage
  en régime établi (point fixe de `vitesses_entree_max`) ; vitesse finale libre.
- Circuit convenable : fermé, sans demi-tour (rotation nette de 180° entre deux lignes droites,
  circulairement), sans croisement ni superposition.

Les notes de réponses au sujet (rédigées à l'origine) sont conservées dans `docs/notes_sujet.md`.
