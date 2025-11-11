from game_engine.fltk import *
from typing import Literal

def main():
    state: Literal["MENU", "GAME", "GAME_OVER"] = "MENU"
    width, height = 900, 700
    
    cree_fenetre(width, height, redimension=True)
    while True:
        event, event_type = donne_ev(), type_ev(donne_ev())
        efface_tout()

        if state == "MENU":
            texte((width / 2) - 130, 60, "WALL IS YOU — MENU")
            texte((width / 2) - 150, 100, "[Enter] to play, [Q] to quit")

            if event_type == "Touche":
                match touche(event):
                    case "Return": state = "GAME"
                    case 'q' | 'Q' | "Escape": break
        
        elif state == "GAME":
            texte((width / 2) - 130, 650, "Game: [Space] movement, [R] reset, [Esc] menu")

            if event_type == "Touche":
                match touche(event):
                    case "Escape": state = "MENU"
                    # case "r": 
                    # case "space":

        elif state == "GAME_OVER":
            texte((width / 2) - 130, 60, "Game Over")
            texte((width / 2) - 150, 100, "[Enter] to play again, [Esc] back to menu")
            
            if event_type == "Touche": 
                match touche(event):
                    case "Escape": state = "MENU"

        mise_a_jour()
            
        attend_clic_gauche()
        ferme_fenetre()
    
if __name__ == '__main__':
    main()