from psychopy import visual, core, event


def basic_window():
    try:
        win = visual.Window(
            size=(800, 600),
            color=[-1, -1, -1],
            units="pix",
            allowGUI=True,
            fullscr=False
        )

        message = visual.TextStim(win, text="Hello from PsychoPy!")
        message.draw()
        win.flip()

        core.wait(20)  # Attendre 2 secondes

        win.close()

    except:
        pass
    """

win = visual.Window(
    size=(1000, 1000),
    color=[-0.5, -0.5, -0.5],
    units="pix"
)

cross = visual.ShapeStim(
    win=win,
    vertices=((0, -10), (0, 10), (0, 0), (-10, 0), (10, 0)),  # Plus petite taille de la croix
    lineWidth=3,
    closeShape=False,
    lineColor="white"
)

cross.draw()
win.flip()

core.wait(10)

win.close()"""