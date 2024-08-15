from psychopy import core, visual, event
timer = core.Clock()
# Créez une fenêtre pour chaque écran
win1 = visual.Window(size=(1920, 1080), fullscr=True, screen=0)
win2 = visual.Window(size=(1920, 1080), fullscr=True, screen=1)

stimulus1 = visual.TextStim(win1, text='Affichage sur écran 1', color=(1, 1, 1))
stimulus2 = visual.TextStim(win2, text='Affichage sur écran 2', color=(1, 1, 1))

print(timer.getTime())
stimulus1.draw()
stimulus2.draw()
print(timer.getTime())
win1.flip()
print(timer.getTime())
win2.flip()


# Attendre une touche pour fermer les fenêtres
event.waitKeys()
win1.close()
win2.close()
