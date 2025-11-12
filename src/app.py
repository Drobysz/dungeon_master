from game_engine.fltk import *
from typing import Literal
from view.MenuView.menu_view import MenuView

def main():
    state: Literal["MENU", "GAME", "GAME_OVER"] = "MENU"
    width, height = 650, 650
    menu = MenuView()
    
    cree_fenetre(width, height)
    menu.render()

    while True:
        event = donne_ev()
        event_type = type_ev(event)
        choice = menu.handle_event(event, event_type)

        if choice:
            if choice["action"] == "start":
                print("Selected level:", choice["level"])
                print("Options:", choice["options"])
            elif choice["action"] == "quit":
                break

        mise_a_jour()
    
if __name__ == '__main__':
    main()