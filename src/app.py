from game_engine.fltk import *
from typing import Literal

from view.MenuView.menu_view import MenuView
from view.GameView.game_view import GameView
from controller.game_controller import GameController

from helpers import list_levels, get_filename

def main():
    state: Literal["MENU", "GAME", "GAME_OVER"] = "MENU"
    width, height = 650, 650
    menu = MenuView()
    game: GameController | None = None
    game_view: GameView | None = None
    savings = { f.name.split('.')[0]: None for f in list_levels() }
    
    cree_fenetre(width, height, redimension=True)

    while True:
        event = donne_ev()
        event_type = type_ev(event)
        match state:
            case "MENU":
                menu.render()
                choice = menu.handle_event(event, event_type)

                if choice:
                    if choice["action"] == "start":
                        lvl = get_filename(choice["level"])
                        
                        opt1 = savings[lvl] is not None
                        opt2 = choice['options']['save_enabled']
                        
                        if opt1 and opt2:
                            game = savings[lvl]
                        else:
                            game = GameController(choice["level"], choice["options"])
                        
                        game_view = GameView(game)
                        state = "GAME"
                    elif choice["action"] == "quit":
                        break
        
            case "GAME":
                if game is None or game_view is None:
                    state = "MENU"
                else:
                    game_view.render()
                    action = game_view.handle_event(event, event_type)
                    
                    match action:
                        case "END_TURN":
                            game.end_turn(game_view.render)
                        case "RESTART":
                            game.reset()
                        case "TO_MENU":
                            if game.options['save_enabled']:
                                lvl = get_filename(game.level_path)
                                savings[lvl] = None if game.game_over else game

                            state = "MENU"

        mise_a_jour()
    
if __name__ == '__main__':
    main()