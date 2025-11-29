

# Wall is You - Documentation

> [!Note]
> J'ai essayé d'expliquer en détail la structure des classes, des méthodes clés et de la fonction.
> Si quelque chose reste peu clair, vous pouvez toujours me contacter personnellement ou via Discord.
> J'espère que vous n'aurez aucune question. Bonne lecture de la documentation !

> [!Important]
> La langue originale de cette documentation est le russe
> Pour la traduction vers d'autres langues, j'ai utilisé Deepl afin de gagner du temps
> Si certaines phrases vous paraissent peu claires ou étranges, vous pouvez me contacter pour des précisions

## Content

- ### [Hierarchy](#Hierarchy)
- ### [Overview of classes](#Overview-of-classes)
- ### [Entities](#Entities)
- ### [Game field class (Dungeon)](#Game-field-class-(Dungeon))
- ### [Level parser method](#Level-parser-method)
- ### [Game Controller](#Game-Controller)
- ### [Menu (app.py)](#Menu-(app.py))
- ### [Menu View](#Menu-View)
- ### [Game View](#Game-View)


## Hierarchy

- App
	- Menu View
	- Game View
		- Game controller
			- Dungeon
				- Cell

<br>

## Overview of classes

1. ***Menu View*** et ***Game View*** sont responsables pour:
-  le rendu du menu et du jeu
-  la gestion des événements (appuis sur les touches et clics de souris)

2. ***Cell** - un objet cellulaire avec des états « mur » et une méthode pour le retourner.

3. ***Dungeon*** - un objet composé d'instances de la classe Cell. Il dispose de méthodes permettant de rechercher des voisins et de vérifier la présence de couloirs communs. Il s'agit en fait d'une carte de niveau.

4. ***Game controller*** - est l'objet qui stocke l'état du jeu et l'instance Dungeon (carte / matrice avec des cellules et leurs états). Il peut également calculer le chemin suivant et traiter le passage du chemin et les rencontres avec les ennemis.

## Entities

### Cell

#### Description
La classe Cell représente une cellule où chaque côté a un état qui montre si un couloir est là (True - présent ; False - absent).

#### Attributes
Les attributs représentent les 4 états du mur.

#### Methodes
```python
def rotate(self)
```
- la méthode renvoie une instance de Cell avec les états des murs tournés dans le sens horaire

<br>

```python
def has_dir(self, directory)
```
- la méthode vérifie la présence d'un couloir dans la direction indiquée en consultant le dictionnaire des états des murs avec la clé de la direction transmise



### Dragon and Hero
Классы Dragon и Hero в качестве аттрибутов имеют позицию и уровень.
> [!IMPORTANT]
> À ce stade du développement, ils sont utilisés comme types via
le décorateur @dataclass.



## Game field class (Dungeon)

### Description
Cette classe représente une matrice d'instances Cell.

### Attributes
En tant qu'attributs, la classe dispose de la matrice susmentionnée, de sa largeur et de sa hauteur calculées.

> [!Warning]
> la largeur et la hauteur seront attribuées
> dans la méthode magique __init__ dans la prochaine version

### Methodes

```python
def in_bound(self, row, column)
```
- la méthode vérifie que les coordonnées ne dépassent pas les limites de la matrice

<br>

```python
def get_cell(self, row, column)
```
- la méthode renvoie l'instance nécessaire par ses coordonnées,
	si les coordonnées ne dépassent pas les limites de la matrice

<br>

```python
def rotate_cell(self, row, column)
```
- la méthode fait tourner la cellule aux coordonnées indiquées

```python
def neighbors(neighbors)
```

1. la méthode parcourt le dictionnaire DIRECTIONS avec la méthode items(), en utilisant les valeurs de décalage pour se déplacer vers une cellule voisine dans les quatre directions dont les noms sont utilisés comme clés

2. Coordonnées de la cellule voisine = coordonnées actuelles + décalages

3. Si les coordonnées de la cellule voisine ne dépassent pas les limites (méthode in_bounds()), elles et leur direction sont renvoyées sous forme de tuple via yield.

<br>

```python
def are_connected(
	self,
	row, column,
	n_row, n_column #neighbor cell coordinates
)
```
- **la méthode vérifie si les cellules voisines sont reliées par des couloirs**

1. d'abord nous obtenons les valeurs de décalage (les mêmes que dans DIRECTIONS)

```python
shifted_row = n_row - row
shifted_col = n_col - col
```

2. ensuite nous parcourons à nouveau DIRECTIONS avec la même méthode
3. à chaque itération nous vérifions si les décalages sur les lignes et les colonnes sont égaux aux décalages de la direction
4. s'ils sont égaux, nous vérifions que les cellules ne sortent pas des limites
5. nous obtenons les instances de Cell par leurs coordonnées et vérifions s'il existe des couloirs dans les directions opposées de ces cellules.



## Level parser method

```python
def load_levels(path)
```
**méthode qui analyse les fichiers json contenant les niveaux

load_levels analyse "grid", crée une matrice d'instances de Cell et, sur cette base,
crée une instance de Dungeon (game field class).

load_levels crée également les objets :
- hero (avec niveau et coordonnées) ;
- dragons (liste de dragons avec les mêmes propriétés que le héros)

tous les objets créés (y compris dungeon) sont renvoyés par la méthode sous forme de tuple



## Game Controller

### Description
Cette classe contient les états du jeu et les entités, ainsi que les fonctionnalités du jeu.

### Attributes
- entities: dragons, hero
- game_over: état de fin de jeu
- options: dictionnaire avec les options choisies dans le menu
- game_result: résultat de la partie
- last_path: dernier chemin calculé du héros

### Methodes

```python
def _load_level(self)
```
- méthode interne qui définit les états initiaux et récupère les valeurs des entities
  depuis le parseur load_levels() du même nom

<br>

```python
def reset(self)
```
- méthode pour réinitialiser les états aux valeurs par défaut afin de recommencer la partie. Pour cela, la méthode appelle _load_level() en interne.

<br>

```python
def is_over(self)
```
- **méthode qui renvoie l'état game_over**

> [!Warning]
> la méthode **is_over** sera supprimée dans la prochaine version
> car elle n'est plus nécessaire

```python
def rotate_cell(self, row, col)
```
**appelle la méthode rotate_cell() de la classe Dungeon**

<br>

```python
def _compute_intention_path(self, max_steps)
```
- **méthode destinée à calculer le prochain chemin / tour.**

1. d'abord, des variables avec les coordonnées du héros sont créées à partir de hero["position"] ;
2. une boucle while s'exécute en ajoutant steps += 1 jusqu'à max_steps ou jusqu'à un break ;
3. next_pos est remis à zéro ;
4. la méthode parcourt en boucle les cellules voisines obtenues via la méthode neighbors de la classe Dungeon ;
5. si la cellule est égale à la précédente (variable "previous"), on la saute
6. via la méthode are_connected de la classe Dungeon nous vérifions la présence de couloirs communs entre les cellules ;
7. s'ils existent, nous affectons les coordonnées à next_pos, puis break ;
8. si après la boucle next_pos reste None, la boucle while s'arrête et la liste "path" actuelle est renvoyée ;
9. la variable "previous" reçoit les coordonnées actuelles, next_pos est ajoutée à "path", steps est incrémenté de 1 et la boucle se répète jusqu'à ce que next_pos devienne None (c'est-à-dire que la boucle arrive dans une impasse).

<br>

```python
def end_turn(self, render)
```
- **la méthode parcourt le chemin calculé et gère les rencontres avec les ennemis.**

> [!Note]
> la méthode render de la classe GameView est passée en paramètre ; elle est responsable de la mise en page de la session de jeu et de la gestion des appuis sur les touches et des clics.

1. la méthode calcule le chemin via _compute_intention_path() et obtient le level du héros.
2. ensuite, une boucle for parcourt les coordonnées du chemin
3. des variables pour le dragon sont définies
4. une autre boucle for parcourt la liste des dragons et compare leurs coordonnées aux coordonnées actuelles. Si elles sont égales, nous récupérons l'id du dragon et son niveau.
5. si le niveau du héros est égal ou supérieur, le dragon avec cet id est supprimé de la liste et son niveau est ajouté au héros ; sinon la partie se termine par la défaite du héros (le statut de la session devient "lose").
6. après la fin du déplacement sur la cellule, le personnage est redessiné.
7. après la boucle, l'état de la session et le nombre de dragons sont vérifiés. Si tous les dragons sont vaincus, le statut "win" est attribué à la session.



## Menu (app.py)

app.py - fichier responsable du basculement entre le menu et la session de jeu.

### States/Variables

1. Au début de la fonction main, une fenêtre est créée et son extension est définie. Un objet menu est également créé, ainsi que des variables pour GameController et GameView.


2.  Dans app.py, il existe une variable d'état du jeu portant le même nom, state.

#### Обзор состоянии переменной state:

1. ***MENU*** - dans cet état, le menu est constamment affiché et les pressions sur les touches et les clics sur les boutons du menu sont traités.
- Événements :
	- **start** (`Enter` ou bouton `Play`) : création des instances de GameController et GameView + transmission des données de session (options sélectionnées) au game controller
	- **quit** (`Esc` ou bouton `Exit`) : quitter le jeu

2. ***Game*** - dans cet état, le rendu du terrain de jeu et le lancement du gestionnaire d'événements de la session de jeu ont lieu.
- Événements :
	- **END_TURN** (`Space`) : effectuer un tour
	- **RESTART** (raccourci `R`) : recommencer la partie
	- **TO_MENU** (`Esc`) : retour au menu



## Menu View

### Utils

```python
def list_levels()
```

- la fonction analyse les noms des fichiers avec l'extension json dans le répertoire levels

```python
LEVELS_DIR = _PROJECT_ROOT / "components" / "levels"
```

<br>

```python
def point_in_rect(
	x, y, # coordonnées où le clic a eu lieu
	rectancle # tuple avec les coordonnées et les dimensions du rectangle
)
```

- la méthode vérifie si les coordonnées du clic se trouvent dans l'intervalle du rectangle


### Attributes

- levels: liste des niveaux ;
- sel (selected): id du niveau sélectionné
- scroll: id du premier niveau visible dans la boîte de la liste des niveaux.
- hit: liste des hitbox des boutons et des options
- hit_items: liste des hitbox des niveaux

### Components

```python
def _button(
    	self,
     	rectangle: Coord, # tuple avec les coordonnées et les dimensions
      	label: str, # texte à l'intérieur du bouton
        props: BtnTypes = "default" # type du bouton
    )
```

- La fonction crée un bouton avec les coordonnées et les dimensions transmises. L'apparence du bouton (couleurs de fond et de bordure) dépend également du props transmis.

```python
def _checkbox(
	self,
	rectangle, # tuple avec les coordonnées et les dimensions
	checked: bool # état d'activation de l'option
)
```

1. comme _button la fonction crée un composant "option"
2. de plus, si checked est true, une coche verte apparaît dans l'option

### Event Handler

```python
def handle_event(
	self,
	event, # événement
	event_type # type d'événement
)
```

Appuis sur les touches :

`Space` | `Return` - **Démarrer la partie**
`q` | `Q` | `Esc`  - **Quitter**
`Up` -    **monter d'une sélection**
`Down` -  **descendre d'une sélection**
`Next` -  **monter de 5 sélections**
`Prior` - **descendre de 5 sélections**

Clics sur les éléments du menu

1. d'abord, ***handle_event*** vérifie si le clic est tombé sur les hitbox de sélection (niveaux).

2. Ensuite, il vérifie les hitbox des boutons :
	- bouton "Play" : la fonction renvoie les états des options, le niveau sélectionné et l'action "start"

	- bouton "Exit" : renvoie l'action "quit"

3. Ensuite, la méthode vérifie les hitbox des options. Si une option est cliquée, son état booléen est inversé et, si l'état est True, une coche apparaît à l'intérieur de l'option.

### Helpers

```python
def _has_selection(self)
```

- la méthode vérifie que l'id du niveau sélectionné ne dépasse pas les limites

<br>

```python
def _toggle_option(self, key)
```

- la méthode inverse l'état de l'option dont la clé est passée en paramètre

<br>

```python
def _move_sel(self, shift)
```

- la méthode décale l'id du niveau sélectionné de shift fois

- ```max(0, min(len(s.levels) - 1, s.sel + shift))``` - cette ligne est destinée à ramener l'id du niveau sélectionné dans l'intervalle si celui-ci en sort après le décalage.

<br>

```python
def _ensure_sel_visible(seld)
```

- la méthode met en surbrillance le niveau sélectionné avec un rectangle bleu
- la méthode ajuste l'affichage des niveaux dans la boîte de liste

```python
s.scroll = max(0, min(s.scroll, max(0, len(s.levels) - visible)))
```

- cette ligne de la méthode `_ensure_sel_visible()` est destinée à ramener scroll dans l'intervalle si sa valeur sort des limites après le décalage.

```python
max(0, len(s.levels) - visible)
```

- le nombre de niveaux qui n'ont pas tenu dans la boîte de la liste des niveaux.



## Game View

### Attributes

```python
def _grid_to_pixel(self, row, col)
```

- conversion des coordonnées de cellule dans la matrice en coordonnées en pixels

<br>

```python
def _pixel_to_grid(self, x, y)
```

- conversion des coordonnées en pixels en coordonnées dans la matrice

<br>

```python
def _grid_center(self, row, col)
```

- la méthode renvoie les coordonnées du centre de la cellule en pixels

<br>

### Event Handler

#### Appuis sur les touches

1. en cas de fin de la session de jeu :
- `Return` | `Space` | `r` | `R` | `Space` : redémarrer la partie
- `Esc` : retour au menu

2. pendant le jeu :
- `Space` : effectuer un tour
- `r` | `R` : redémarrer la partie
- `Esc` : retour au menu

#### Clic gauche de la souris

1. À l'aide des fonctions `abscisse` et `ordonnee` nous obtenons les coordonnées
2. Nous les convertissons via `_pixel_to_grid` en coordonnées de la matrice.
3. Si les coordonnées ne dépassent pas les limites, nous transmettons les coordonnées converties à la méthode `rotate_cell` pour tourner la cellule de 90 degrés.