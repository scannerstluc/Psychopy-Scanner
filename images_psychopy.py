import argparse
from psychopy import visual, core, event

def affichage_mots(win, text_stim, words, display_time):
    for word in words:
        text_stim.setText(word)
        text_stim.draw()
        win.flip()
        core.wait(display_time)

def reading(filename):
    filename= filename
    with open(filename, "r") as fichier:
        ma_liste = [line.strip() for line in fichier]
    print(ma_liste)
    return ma_liste

def words_psychopy(words, display_time, boolean):
    print(words)
    """
    win = visual.Window(fullscr=True, color=[-1, -1, -1], units='pix')
    if boolean:
        text_stim = visual.TextStim(win, text='', color=[1, 1, 1], height=150)
    else:
        text_stim = visual.TextStim(win, text='', color=[1, 1, 1], height=50)
    text_stim.setText("")
    text_stim.draw()
    win.flip()
    event.waitKeys()
    nothinkinglist = [":; $+", " #^=-", ":?$µ", "###"]
    affichage_mots(win, text_stim, nothinkinglist, display_time)
    affichage_mots(win, text_stim, words, display_time)
    affichage_mots(win, text_stim, nothinkinglist, display_time)
    event.waitKeys()
    win.close()
    core.quit()
    """

def static_images_psychopy(chemin,duration):
    chemin = "Paradigme_images_statiques/"+chemin
    images = reading(chemin)

    win = visual.Window(
        fullscr=True,
        color=[-0.0118, 0.0039, -0.0196],
        units="pix"
    )

    # Créer le stimulus de croix
    cross_stim = visual.ShapeStim(
        win=win,
        vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
        lineWidth=3,
        closeShape=False,
        lineColor="white"
    )

    cross_stim.draw()
    win.flip()
    event.waitKeys()

    for image in images:
        chemin = "Paradigme_images_statiques/stim_static/" + image
        print(chemin)
        image_stim = visual.ImageStim(
            win=win,
            image=chemin,  # Remplacez par le chemin de votre image
            pos=(0, 0)  # Position centrale
        )
        image_stim.size *= 0.5
        # image_stim.ori=45
        # Dessiner l'image
        image_stim.draw()
        win.flip()
        core.wait(duration)
        cross_stim.draw()
        win.flip()
        core.wait(2 * duration)
    win.close()

def main(duration,file):
    print(f"Durée: {duration}")
    if file !="":
        static_images_psychopy(file,duration)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=str, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file",required=False, type=str, help="Liste de mots pour le paradigme")
    args = parser.parse_args()

    print("on arrive jamais ici")
    main(int(args.duration), args.file)
