import argparse
import csv

from psychopy import visual, core, event
import serial


def wait_for_trigger(port='COM3', baudrate=9600, trigger_char='s'):
    with serial.Serial(port, baudrate=baudrate) as ser:
        trigger = ser.read().decode('utf-8')
        while trigger != trigger_char:
            trigger = ser.read().decode('utf-8')
        print("Trigger received")


def reading(filename):
    filenames = []
    angles = []
    with open(filename, "r") as fichier:
        for line in fichier:
            parts = line.strip().split(',')
            if len(parts) == 2:
                filenames.append(parts[0].strip())
                angles.append(int(parts[1].strip()))
    return filenames, angles

def static_images_psychopy(chemin, duration, betweenstimuli, zoom):
    win = visual.Window(
        fullscr=True,
        color=[-0.0118, 0.0039, -0.0196],
        units="pix"
    )
    chemin = "Paradigme_images_statiques/" + chemin
    images, orientation = reading(chemin)
    cross_stim = visual.ShapeStim(
        win=win,
        vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
        lineWidth=3,
        closeShape=False,
        lineColor="white"
    )
    thezoom = 0.8+(0.3*zoom/100)
    #thezoom = 1 if zoom else 0.5
    timer = core.Clock()  # Horloge pour le timing précis
    stimulus_times = []  # Liste pour enregistrer les moments des stimuli
    stimulus_apparition=[]
    stimuli_liste = []
    cross_stim.draw()
    win.flip()
    wait_for_trigger()
    global_timer = core.Clock()
    count = 0
    for image in images:
        image_path = "Paradigme_images_statiques/stim_static/" + image
        image_stim = visual.ImageStim(
            win=win,
            image=image_path,
            pos=(0, 0),
            size=None  # Utilisez None pour conserver la taille originale ou ajustez selon 'thezoom'
        )
        image_stim.size *= thezoom
        image_stim.ori = orientation[count]

        image_stim.draw()
        win.flip()
        stimulus_apparition.append(global_timer.getTime())
        timer.reset()  # Réinitialiser le timer à chaque nouvelle image
        while timer.getTime() < duration:
            pass
        stimulus_times.append(timer.getTime())
        stimuli_liste.append(image)

        # Afficher la croix entre les images
        cross_stim.draw()
        win.flip()
        stimulus_apparition.append(global_timer.getTime())
        timer.reset()
        while timer.getTime() < betweenstimuli:
            pass
        stimulus_times.append(timer.getTime())
        stimuli_liste.append("Fixation")
        count+=1




    win.close()
    return stimulus_times, stimulus_apparition,stimuli_liste, orientation

def write_tsv(onset, duration, file_stimuli, orientation, trial_type, filename="output.tsv"):
    with open(filename, mode='w', newline='') as file:
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow(['onset', 'duration', 'trial_type','angle', 'stim_file', ])
        orientation.insert(3,0)
        for x in range (len(trial_type)):
            if trial_type[x]=="Fixation":
                orientation.insert(x,"None")
        for i in range(len(onset)):
            tsv_writer.writerow([onset[i], duration[i], trial_type[i], orientation[i], file_stimuli[i]])


def main(duration, betweenstimuli, file, zoom, output_file):
    stimulus_times, stimulus_apparition, stimuli, orientation = static_images_psychopy(file, duration, betweenstimuli, zoom)
    liste_trial=[]
    liste_lm=[]
    count=0
    for x in stimuli:
        if x == "Fixation":
            liste_lm.append(count)
            liste_trial.append("Fixation")
        else:
            liste_trial.append("Stimuli")
        count+=1
    for x in liste_lm:
        stimuli[x] = "None"
    write_tsv(stimulus_apparition, stimulus_times, stimuli, orientation, liste_trial, output_file)


print(reading("Paradigme_images_statiques/Sequence1.txt"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=int, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=int, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")

    args = parser.parse_args()

    main(args.duration, args.betweenstimuli, args.file, args.zoom, "Fichiers_output/"+args.output_file+".tsv")