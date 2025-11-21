from game_engine.fltk import *
from typing import Literal
from view.MenuView.menu_view import MenuView
from view.GameView.game_view import GameView
from controller.game_controller import GameController

def main():
    state: Literal["MENU", "GAME", "GAME_OVER"] = "MENU"
    width, height = 650, 650
    menu = MenuView()
    game: GameController | None = None
    game_view: GameView | None = None
    
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
                            game.end_turn()
                        case "RESTART":
                            game.reset()
                        case "TO_MENU":
                            state = "MENU" 

        mise_a_jour()
    
if __name__ == '__main__':
    main()