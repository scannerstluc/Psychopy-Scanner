import argparse
import csv
import os
from datetime import datetime

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
        #color=[-0.0118, 0.0039, -0.0196],
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
    timer = core.Clock()  # Horloge réinitialisée à chaque stimuli
    stimulus_times = []  # Liste pour enregistrer la durée des stimuli
    stimulus_apparition=[] #Liste pour enregistrer le timing d'apparition des stimuli
    stimuli_liste = [] #Liste pour enregistrer les noms des stimuli, si c'est une croix ce sera Fixation sinon le nom du fichier
    cross_stim.draw()
    win.flip()
    liste_image_win = []
    count = 0
    for image in images:
        image_path = "Paradigme_images_statiques/stim_static/" + image
        image_stim = visual.ImageStim(
            win=win,
            image=image_path,
            pos=(0, 0),
            size=None
        )
        image_stim.size *= thezoom
        image_stim.ori = orientation[count]
        liste_image_win.append(image_stim)
        stimuli_liste.append(image)
        stimuli_liste.append("Fixation")
        count+=1


    wait_for_trigger() #Attente du signal pour commencer l'expérience, en attendant une croix sera affichée au centre
    global_timer = core.Clock() #Horloge principale

    for image_stim in liste_image_win:
        image_stim.draw()
        win.flip()
        stimulus_apparition.append(global_timer.getTime())
        timer.reset()  # Réinitialiser le timer à chaque nouvelle image
        while timer.getTime() < duration:
            pass
        stimulus_times.append(timer.getTime())

        cross_stim.draw()
        win.flip()
        stimulus_apparition.append(global_timer.getTime())
        timer.reset() # Réinitialiser le timer à chaque nouvelle image
        while timer.getTime() < betweenstimuli:
            pass
        stimulus_times.append(timer.getTime())
    win.close()
    return stimulus_times, stimulus_apparition,stimuli_liste, orientation

def write_tsv(onset, duration, file_stimuli, orientation, trial_type, filename="output.tsv"):
    output_dir = 'Fichiers_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    current_date = datetime.now().strftime("%Y-%m-%d")
    run_number = 1
    filename_prefix = f"{current_date}_{filename.split('.')[0]}"
    existing_files = [f for f in os.listdir(output_dir) if f.startswith(filename_prefix) and 'run' in f]
    if existing_files:
        runs = [int(f.split('run')[-1].split('.')[0]) for f in existing_files if 'run' in f]
        if runs:
            run_number = max(runs) + 1
    filename = os.path.join(output_dir, f"{filename_prefix}_run{run_number}.tsv")



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

    main(args.duration, args.betweenstimuli, args.file, args.zoom, args.output_file)