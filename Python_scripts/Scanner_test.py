from psychopy import core, visual, event
timer = core.Clock()

win0 = visual.Window(size=(1920, 1080), fullscr=True, screen=0)
win1 = visual.Window(size=(1920, 1080), fullscr=True, screen=1)
#win2 = visual.Window(size=(1920, 1080), fullscr=True, screen=2)
#win3 = visual.Window(size=(1920, 1080), fullscr=True, screen=3)

stimulus0 = visual.TextStim(win0, text='Affichage sur écran 0', color=(1, 1, 1))
stimulus1 = visual.TextStim(win1, text='Affichage sur écran 1', color=(1, 1, 1))
#stimulus2 = visual.TextStim(win2, text='Affichage sur écran 2', color=(1, 1, 1))
#stimulus3 = visual.TextStim(win3, text='Affichage sur écran 3', color=(1, 1, 1))

stimulus1.draw()
#stimulus2.draw()
#stimulus3.draw()
stimulus0.draw()

win1.flip()
#win2.flip()
#win3.flip()
win0.flip()


event.waitKeys()
win1.close()
win0.close()