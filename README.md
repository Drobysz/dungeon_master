# Dungeon Master (Wall is You) 
__documentation on original launguage__<br>
A project implemented in the frame of BUT Info coursework SAE 101

## Content

### - [Description](#Description)
### - [Launch](#Launch)
### - [Rules of the game](#Rules-of-the-game)
### - [Controls](#Controls)
### - [Format of levels](#Format-of-levels)
### - [Members](#Members)

## Description

A Python game using the FLTK educational library.
The player rotates the dungeon rooms so that the hero can reach all the dragons through the corridors.
After each dungeon move, the hero automatically follows their “intention” (through accessible corridors), fights dragons, and levels up.

## Launch

```bash
python3 app.py
```

## Dependencies

- [python 3.12](https://www.python.org/downloads/release/python-31210/)
- university interface library [fltk](./src/game_engine/fltk.py)

## Rules of the game

- The dungeon consists of cells-rooms, each of which may have corridors leading up/right/down/left.
- The player can rotate rooms to form a path for the hero.
- After pressing `Space`, the hero automatically walks along the corridors (“intention”) as long as he can.
- In each room, the hero may encounter a dragon:
  - if the hero's level is ≥ the dragon's level, the hero wins, their level increases, and the dragon disappears;
  - otherwise, the hero dies and the game ends in defeat.
- The goal is to destroy all the dragons and survive.

> [!WARNING]
> A corridor in the game is a blue line. From a UI/UX design perspective, this may not be obvious.
> In next versions of the game this flaw will be rectified.

## Controls

```md
### In the menu

- `↑/↓` — select level
- `Enter` — start game
- `LMB` — switch options (treasures, dragon movement, save)
- `Q` or `Esc` — exit game

### In the game

- `LMB` on the room — rotate the room 90° clockwise
- `Space` — complete the dungeon move and perform the hero's move
- `R` — restart the current level
- `Esc` — return to the menu

After completing the game (victory/defeat):

- `Enter` / `R` — restart the level
- `Esc` — return to the menu
```

## Format of levels

Levels are stored in `components/levels/*.json`.

Example:

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

## Members

- **Alexander Drobyshevski**: main developer
  - [portfolio site](https://drobysz.vercel.app/projects)
  - [linkedin](https://www.linkedin.com/in/alexander-drobyshevski-9656b2330)
- **Millan Lechar**: assistent developer