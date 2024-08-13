from psychopy import visual, event

# Initialiser la fenêtre
win = visual.Window([800, 600])

# Initialiser la souris
mouse = event.Mouse(win=win)


while True:
    # Obtenir l'état des boutons de la souris
    buttons = mouse.getPressed()

    # Afficher l'état des boutons (un tableau avec 3 éléments : gauche, milieu, droite)
    print(buttons)

    # Si un bouton est pressé, sortir de la boucle
    if any(buttons):
        print("Bouton de la souris pressé !")
        break

    # Rafraîchir la fenêtre
    win.flip()
