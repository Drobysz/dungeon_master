# Dungeon Master (Wall is You)
**__trandlated with Deelp into french__**
Un projet réalisé dans le cadre du cours BUT Info SAE 101

## Contenu

### - [Description](#Description)
### - [Lancement](#Lancement)
### - [Règles du jeu](#Règles-du-jeu)
### - [Controls](#Controls)
### - [Format des niveaux](#Format-des-niveaux)
### - [Membres](#Membres)

## Description

Jeu Python utilisant la bibliothèque éducative FLTK.
Le joueur fait pivoter les salles du donjon afin que le héros puisse atteindre tous les dragons à travers les couloirs.
Après chaque déplacement dans le donjon, le héros suit automatiquement son « intention » (à travers les couloirs accessibles), combat les dragons et gagne des niveaux.

## Lancement

```bash
python3 app.py
```

## Dependencies

- python 3.12
- university interface library fltk

## Règles du jeu

- Le donjon est composé de cellules-pièces, chacune pouvant avoir des couloirs menant vers le haut/la droite/le bas/la gauche.
- Le joueur peut faire pivoter les pièces pour former un chemin pour le héros.
- Après avoir appuyé sur la touche « Espace », le héros marche automatiquement dans les couloirs (« intention ») aussi longtemps qu'il le peut.
- Dans chaque pièce, le héros peut rencontrer un dragon :
  - si le niveau du héros est ≥ au niveau du dragon, le héros gagne, son niveau augmente et le dragon disparaît ;
  - sinon, le héros meurt et le jeu se termine par une défaite.
- Le but est de détruire tous les dragons et de survivre.

## Controls

```md
### Dans le menu

- `↑/↓` — select level
- `Enter` — start game
- `LMB` — switch options (treasures, dragon movement, save)
- `Q` or `Esc` — exit game

### Dans le jeu

- `LMB` on the room — rotate the room 90° clockwise
- `Space` — complete the dungeon move and perform the hero's move
- `R` — restart the current level
- `Esc` — return to the menu

Après avoir terminé le jeu (victory/defeat):

- `Enter` / `R` — restart the level
- `Esc` — return to the menu
```

## Format des niveaux

Niveaux sont contenus dans `components/levels/*.json`.

Exemple:

```json
{
  "grid": [
    [
      { "top": false, "right": true,  "bottom": false, "left": true },
      { "top": false, "right": false, "bottom": true,  "left": false }
    ],
    ...
  ],
  "hero": {
    "row": 0,
    "col": 0,
    "level": 1
  },
  "dragons": [
    { "row": 2, "col": 3, "level": 1 },
    { "row": 4, "col": 1, "level": 2 }
  ]
}
```

## Membres

- **Alexander Drobyshevski**: développeur principal
- **Millan Lechar**: développeur assistant