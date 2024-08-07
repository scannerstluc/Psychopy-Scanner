import argparse
import serial
from psychopy import visual, core, event


def wait_for_trigger(port='COM3', baudrate=9600, trigger_char='s'):
    with serial.Serial(port, baudrate=baudrate) as ser:
        trigger = ser.read().decode('utf-8')
        while trigger != trigger_char:
            trigger = ser.read().decode('utf-8')
        print("Trigger received")


def affichage_mots(win, text_stim, words, display_time):
    timer = core.Clock()
    for word in words:
        text_stim.setText(word)
        text_stim.draw()
        win.flip()
        timer.reset()  # Réinitialiser l'horloge à chaque nouveau mot
        while timer.getTime() < display_time:
            pass  # Attendre sans bloquer d'autres processus


def reading(filename):
    filename = "Paradigme_mots/" + filename
    with open(filename, "r") as fichier:
        ma_liste = [line.strip() for line in fichier]
    print(ma_liste)
    return ma_liste


def pause_for_seconds(seconds):
    timer = core.Clock()
    timer.reset()
    while timer.getTime() < seconds:
        pass


def words_psychopy(words, display_time, boolean):
    win = visual.Window(fullscr=True, color=[-1, -1, -1], units='pix')
    text_stim = visual.TextStim(win, text='', color=[1, 1, 1], height=150 if boolean else 50)

    wait_for_trigger()
    nothinkinglist = [":; $+", " #^=-", ":?$µ", "###"]
    affichage_mots(win, text_stim, nothinkinglist, display_time)
    affichage_mots(win, text_stim, words, display_time)
    affichage_mots(win, text_stim, nothinkinglist, display_time)
    pause_for_seconds(5)  # Pause de 5 secondes avant de fermer

    win.close()
    core.quit()


def main(duration, words, zoom, file):
    print(f"Durée: {duration}")
    if file:
        words = reading(file)
    else:
        words = [word.strip() for word in words.split(',')]

    #wait_for_trigger()
    words_psychopy(words, int(duration), zoom == "Activé")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=str, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--words", type=str, required=True, help="Liste de mots pour le paradigme")
    parser.add_argument("--zoom", type=str, choices=['Activé', 'Désactivé'], required=True, help="Activer le Zoom")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)

    args = parser.parse_args()
    main(args.duration, args.words, args.zoom, args.file)
