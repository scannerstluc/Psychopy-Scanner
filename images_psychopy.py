import argparse
from psychopy import visual, core, event
import serial


def wait_for_trigger(port='COM3', baudrate=9600, trigger_char='s'):
    with serial.Serial(port, baudrate=baudrate) as ser:
        trigger = ser.read().decode('utf-8')
        while trigger != trigger_char:
            trigger = ser.read().decode('utf-8')
        print("Trigger received")


def reading(filename):
    with open(filename, "r") as fichier:
        ma_liste = [line.strip() for line in fichier]
    return ma_liste


def static_images_psychopy(chemin, duration, betweenstimuli, zoom):
    win = visual.Window(
        fullscr=True,
        color=[-0.0118, 0.0039, -0.0196],
        units="pix"
    )
    chemin="Paradigme_images_statiques/"+chemin
    images = reading(chemin)
    cross_stim = visual.ShapeStim(
        win=win,
        vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
        lineWidth=3,
        closeShape=False,
        lineColor="white"
    )
    thezoom = 1 if zoom else 0.5
    timer = core.Clock()  # Horloge pour le timing précis

    cross_stim.draw()
    win.flip()
    wait_for_trigger()

    for image in images:
        image_path = "Paradigme_images_statiques/stim_static/" + image
        image_stim = visual.ImageStim(
            win=win,
            image=image_path,
            pos=(0, 0),
            size=None  # Utilisez None pour conserver la taille originale ou ajustez selon 'thezoom'
        )
        image_stim.size *= thezoom

        image_stim.draw()
        win.flip()
        timer.reset()  # Réinitialiser le timer à chaque nouvelle image
        while timer.getTime() < duration:
            pass  # Attente active jusqu'à la fin de la durée

        # Afficher la croix entre les images
        cross_stim.draw()
        win.flip()
        timer.reset()
        while timer.getTime() < betweenstimuli:
            pass  # Attente active entre les images

    win.close()


def main(duration, betweenstimuli, file, zoom):
    #wait_for_trigger()
    static_images_psychopy(file, duration, betweenstimuli, zoom)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=int, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=int, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=str, choices=['Activé', 'Désactivé'], required=True,
                        help="Activer ou désactiver le Zoom")
    args = parser.parse_args()

    main(args.duration, args.betweenstimuli, args.file, args.zoom == 'Activé')
