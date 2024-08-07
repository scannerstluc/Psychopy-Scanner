import argparse
from psychopy import visual, core, event

def affichage_mots(win, text_stim, words, display_time):
    for word in words:
        text_stim.setText(word)
        text_stim.draw()
        win.flip()
        core.wait(display_time)

def reading(filename):
    filename= "Paradigme_mots/" + filename
    with open(filename, "r") as fichier:
        ma_liste = [line.strip() for line in fichier]
    print(ma_liste)
    return ma_liste

def run_psychopy(words, display_time, boolean):
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
def main(duration, words, zoom, file):
    print(f"Durée: {duration}")
    if file !="":
        words=reading(file)
        if (zoom == "Activé"):
            run_psychopy(words, int(duration), True)
        else:
            run_psychopy(words, int(duration), False)
    else:
        split_list = words.split(',')
        cleaned_list = [item.strip() for item in split_list]
        if (zoom=="Activé"):
            run_psychopy(cleaned_list,int(duration),True)
        else:
            run_psychopy(cleaned_list,int(duration),False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=str, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--words", type=str, required=True, help="Liste de mots pour le paradigme")
    parser.add_argument("--zoom", type=str, choices=['Activé', 'Désactivé'], required=True, help="Activer le Zoom")
    parser.add_argument("--file",required=False, type=str, help="Liste de mots pour le paradigme")


    print("wtf dude")

    args = parser.parse_args()
    print(args.file)


    main(args.duration, args.words, args.zoom, args.file)
