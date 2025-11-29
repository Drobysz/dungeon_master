

# Wall is You - Documentation

> [!Note]
> I tried to explain the structure of the classes, key methods and the function in detail.
> If something is still unclear, you can always contact me personally or via Discord.
> I hope you will have no questions. Enjoy reading the documentation!

> [!Important]
> The original language of this documentation is Russian
> To translate it into other languages I used Deepl to save time
> If any phrases seem unclear or strange, you can contact me for clarification

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

1. ***Menu View*** and ***Game View*** are responsible for:
-  rendering of the menu and the game
-  event handling (key presses and mouse clicks)

2. ***Cell*** is a cell object with wall states and a method for flipping it..

3. ***Dungeon*** is an object consisting of instances of the Cell class. It has methods for finding neighbors and checking for shared corridors. Essentially, it represents a level map.

4. ***Game controller*** is an object that stores the game state and an instance of Dungeon (a map/matrix with cells and their states). It can also calculate the next path and handle path traversal and encounters with enemies.

## Entities

### Cell

#### Description
The Cell class represents a cell where each side has a state indicating the presence of a corridor (True - present; False - absent).

#### Attributes
Attributes represent the four states of the wall.

#### Methodes
```python
def rotate(self)
```
- the method returns a Cell instance with the wall states rotated clockwise

<br>

```python
def has_dir(self, directory)
```
- the method checks whether there is a corridor in the given direction by looking up the wall state dictionary using the passed direction key



### Dragon and Hero
The Dragon and Hero classes have position and level as attributes.
> [!IMPORTANT]
> At this stage of development they are used as types via
the @dataclass decorator.



## Game field class (Dungeon)

### Description
This class represents a matrix of Cell instances.

### Attributes
As attributes, the class has the aforementioned matrix, its calculated width and height.

> [!Warning]
> the width and height will be assigned
> in the __init__ magic method in the next version

### Methodes

```python
def in_bound(self, row, column)
```
- the method checks whether the coordinates are within the bounds of the matrix

<br>

```python
def get_cell(self, row, column)
```
- the method returns the required instance by its coordinates,
	if the coordinates are within the bounds of the matrix

<br>

```python
def rotate_cell(self, row, column)
```
- the method rotates the cell at the given coordinates

```python
def neighbors(neighbors)
```

1. the method iterates over the DIRECTIONS dictionary via the items() method, using the offset values to move to a neighboring cell in four directions whose names are used as keys

2. Neighbor cell coordinates = current + offsets

3. If the neighbor coordinates are within the bounds (in_bounds() method), then via yield they and their direction are returned as a tuple.

<br>

```python
def are_connected(
	self,
	row, column,
	n_row, n_column #neighbor cell coordinates
)
```
- **the method checks whether the neighboring cells are connected by corridors**

1. first we get the offset values (the same as in DIRECTIONS)

```python
shifted_row = n_row - row
shifted_col = n_col - col
```

2. then we again iterate over DIRECTIONS with the same method
3. on each iteration we check whether the row and column offsets are equal to the direction offsets
4. if they are equal, we check that the cells are within bounds
5. we get the Cell instances by their coordinates and check whether there are corridors in the opposite directions of these cells.



## Level parser method

```python
def load_levels(path)
```
**method that parses json files with levels

load_levels parses "grid", creates a matrix of Cell instances, and based on it
creates a Dungeon instance (game field class).

load_levels also creates:
- hero (with level and coordinates);
- dragons (a list of dragons with the same properties as the hero)

all created objects (including dungeon) are returned by the method as a tuple



## Game Controller

### Description
This class contains game states and entities, as well as game functionality.

### Attributes
- entities: dragons, hero
- game_over: состояние окончании игры
- options: словарь с опциями, выбранными в меню
- game_result: результат игры
- last_path: последний просчитанный путь героя

### Methodes

```python
def _load_level(self)
```
- internal method that sets the initial state and gets the entities
  from the load_levels() parser of the same name

<br>

```python
def reset(self)
```
- method to reset the state to default values in order to start the game again. For this, the method calls _load_level() inside itself.

<br>

```python
def is_over(self)
```
- **method that returns the game_over state**

> [!Warning]
> the **is_over** method will be removed in the next version
> because it is no longer needed

```python
def rotate_cell(self, row, col)
```
**calls the Dungeon class rotate_cell() method**

<br>

```python
def _compute_intention_path(self, max_steps)
```
- **method intended to compute the next path / turn.**

1. first, variables with the hero coordinates are created from hero["position"];
2. a while loop runs adding steps += 1 up to max_steps or until break;
3. next_pos is reset;
4. the method iterates over neighboring cells obtained via the Dungeon neighbors method;
5. if a cell is equal to the previous one (the "previous" variable), we skip it
6. using the Dungeon are_connected method we check whether the cells have a common corridor;
7. if they do, we assign the coordinates to next_pos, then break;
8. if after the loop next_pos is still None, the while loop stops and the current "path" list is returned;
9. the "previous" variable is assigned the current coordinates and next_pos is added to "path", steps is incremented by 1 and the loop repeats until next_pos becomes None (i.e. the loop reaches a dead end).

<br>

```python
def end_turn(self, render)
```
- **the method walks along the computed path and handles encounters with enemies.**

> [!Note]
> the render method of the GameView class is passed as a parameter; it is responsible for rendering the game session and handling key presses and clicks.

1. the method computes the path via _compute_intention_path() and gets the hero level.
2. then a for loop iterates over the path coordinates
3. variables for the dragon are defined
4. another for loop iterates over the list of dragons and compares their coordinates to the current ones. If they match, we retrieve the dragon id and its level.
5. if the hero level is equal to or higher, the dragon with that id is removed from the list and its level is added to the hero; otherwise the game ends with the hero's defeat (the session status becomes "lose").
6. after moving to the cell the character is re-rendered.
7. after the loop, the session status and the number of dragons are checked. If all dragons are defeated, the session is given the "win" status.



## Menu (app.py)

app.py - The file responsible for switching between the menu and the game session.

### States/Variables

1. At the beginning of the main function, a window is created and its size is set. A menu object is also created, and variables are created for GameController and GameView.


2.  In app.py, there is a game state variable with the same name, state.

#### Обзор состоянии переменной state:

1. ***MENU*** - In this state, the menu is constantly rendered and key presses and clicks on menu buttons are processed.
- Events:
	- **start** (`Enter` or `Play` button): creation of GameController and GameView instances + passing the session data (selected options) into the game controller
	- **quit** (`Esc` or `Exit` button): exit from the game

2. ***Game*** - In this state, the game field is rendered and the game session event handler is launched..
- Events:
	- **END_TURN** (`Space`): make a move
	- **RESTART** (shortcut `R`): restart the game
	- **TO_MENU** (`Esc`): back to the menu



## Menu View

### Utils

```python
def list_levels()
```

- function parses the filenames with json extension in the levels directory

```python
LEVELS_DIR = _PROJECT_ROOT / "components" / "levels"
```

<br>

```python
def point_in_rect(
	x, y, # coordinates where the click occurred
	rectancle # tuple with the coordinates and sizes of the rectangle
)
```

- method checks whether the click coordinates are inside the rectangle range


### Attributes

- levels: list of levels;
- sel (selected): id of the selected level
- scroll: id of the first level that is visible in the level list box.
- hit: list of hitboxes of buttons and options
- hit_items: list of hitboxes of levels

### Components

```python
def _button(
    	self,
     	rectangle: Coord, # tuple with coordinates and sizes
      	label: str, # text inside the button
        props: BtnTypes = "default" # button type
    )
```

- The function creates a button using the passed coordinates and sizes. The appearance of the button (background and border colors) also depends on the passed props.

```python
def _checkbox(
	self,
	rectangle, # tuple with coordinates and sizes
	checked: bool # option activation state
)
```

1. like _button the function creates an "option" component
2. also, if checked is true, a green checkmark appears in the option

### Event Handler

```python
def handle_event(
	self,
	event, # event
	event_type # event type
)
```

Key presses:

`Space` | `Return` - **Start the game**
`q` | `Q` | `Esc`  - **Exit**
`Up` -    **up by 1 selection**
`Down` -  **down by 1 selection**
`Next` -  **up by 5 selections**
`Prior` - **down by 5 selections**

Clicks on menu elements

1. first, ***handle_event*** checks whether the click hit the selection hitboxes (levels).

2. Then it checks the button hitboxes:
	- "Play" button: the function returns the option states, the selected level and the "start" action

	- "Exit" button: returns the "quit" action

3. After that the method checks the option hitboxes. If an option is clicked, its boolean state is toggled, and if the state is True a checkmark appears inside the option.

### Helpers

```python
def _has_selection(self)
```

- the method checks whether the id of the selected level is within range

<br>

```python
def _toggle_option(self, key)
```

- the method toggles the state of the option whose key is passed in the parameters

<br>

```python
def _move_sel(self, shift)
```

- the method shifts the id of the selected level by shift

- ```max(0, min(len(s.levels) - 1, s.sel + shift))``` - this line is intended to bring the selected level id back into range in case it goes out of range after shifting.

<br>

```python
def _ensure_sel_visible(seld)
```

- the method highlights the selected level with a blue rectangle
- the method adjusts which levels are shown in the list box

```python
s.scroll = max(0, min(s.scroll, max(0, len(s.levels) - visible)))
```

- this line of the `_ensure_sel_visible()` method is intended to bring scroll back into range in case it goes out of range after shifting.

```python
max(0, len(s.levels) - visible)
```

- the number of levels that did not fit into the levels list box.



## Game View

### Attributes

```python
def _grid_to_pixel(self, row, col)
```

- conversion of cell coordinates in the matrix to pixel coordinates

<br>

```python
def _pixel_to_grid(self, x, y)
```

- conversion of cell coordinates in pixels to matrix coordinates

<br>

```python
def _grid_center(self, row, col)
```

- the method returns the center coordinates of a cell in pixels

<br>

### Event Handler

#### Key presses

1. if the game session is over:
- `Return` | `Space` | `r` | `R` | `Space` : restart the game
- `Esc` : back to the menu

2. during the game:
- `Space` : make a move
- `r` | `R` : restart the game
- `Esc` : back to the menu

#### Left mouse click

1. Using the functions `abscisse` and `ordonnee` we get the coordinates
2. We convert them via `_pixel_to_grid` into matrix coordinates.
3. If the coordinates are within range, we pass the converted coordinates to the `rotate_cell` method to rotate the cell by 90 degrees.