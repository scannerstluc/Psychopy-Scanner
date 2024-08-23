import argparse
import csv
import os
from datetime import datetime

from Paradigme_parent import Parente
from psychopy import visual, core, event
import serial



class static_image(Parente):
    def __init__(self, duration, betweenstimuli, file, zoom, trigger, output):
        self.duration = duration #args.duration, args.betweenstimuli, args.file, args.zoom, args.port, args.baudrate, args.trigger  ,args.output_file)
        self.betweenstimuli = betweenstimuli
        self.file = file
        self.zoom = zoom
        self.trigger = trigger
        self.click_times = []
        self.win = win = visual.Window(
            fullscr=True,
            #color=[-0.0118, 0.0039, -0.0196],
            units="pix"
        )
        self.mouse = event.Mouse(win=self.win)
        event.globalKeys.add(key='escape', func=self.win.close)
        self.output = output



    def reading(self, filename):
        filenames = []
        angles = []
        with open(filename, "r") as fichier:
            for line in fichier:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    filenames.append(parts[0].strip())
                    angles.append(int(parts[1].strip()))
        return filenames, angles

    def static_images_psychopy(self, chemin, duration, betweenstimuli, zoom, trigger):
        chemin = "Input/Paradigme_images_statiques/" + chemin
        images, orientation = self.reading(chemin)
        cross_stim = visual.ShapeStim(
            win=self.win,
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
        self.win.flip()
        liste_image_win = []
        count = 0
        for image in images:
            image_path = "Input/Paradigme_images_statiques/stim_static/" + image
            image_stim = visual.ImageStim(
                win=self.win,
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


        super().wait_for_trigger("s")
        global_timer = core.Clock() #Horloge principale

        for image_stim in liste_image_win:
            image_stim.draw()
            self.win.flip()
            stimulus_apparition.append(global_timer.getTime())
            timer.reset()  # Réinitialiser le timer à chaque nouvelle image
            clicked = False  # Variable pour vérifier si un clic a été détecté
            clicked_time = "None"
            while timer.getTime() < duration:
                button = self.mouse.getPressed()  # Mise à jour de l'état des boutons de la souris

                if any(button):
                    if not clicked:  # Vérifier si c'est le premier clic détecté
                        clicked_time = timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True  # Empêcher l'enregistrement de clics multiple
            stimulus_times.append(timer.getTime())

            cross_stim.draw()
            self.win.flip()
            self.click_times.append(clicked_time)
            stimulus_apparition.append(global_timer.getTime())
            timer.reset() # Réinitialiser le timer à chaque nouvelle image
            while timer.getTime() < betweenstimuli:
                pass
            stimulus_times.append(timer.getTime())
            self.click_times.append("None")
        self.win.close()
        return stimulus_times, stimulus_apparition,stimuli_liste, orientation

    def write_tsv(self, onset, duration, file_stimuli, orientation, trial_type, filename="output.tsv"):
        output_dir = '../Fichiers_output'
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
            tsv_writer.writerow(['onset', 'duration', 'trial_type','angle','reaction', 'stim_file', ])
            orientation.insert(3,0)
            for x in range (len(trial_type)):
                if trial_type[x]=="Fixation":
                    orientation.insert(x,"None")
            for i in range(len(onset)):
                tsv_writer.writerow([onset[i], duration[i], trial_type[i], orientation[i], self.click_times[i], file_stimuli[i]])


    def lancement(self):
        stimulus_times, stimulus_apparition, stimuli, orientation = self.static_images_psychopy(self.file, self.duration, self.betweenstimuli, self.zoom, self.trigger)
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
        self.write_tsv(stimulus_apparition, stimulus_times, stimuli, orientation, liste_trial, self.output)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument('--trigger', type=str, required=True, help="caractère pour lancer le programme")

    args = parser.parse_args()

    images = static_image(args.duration, args.betweenstimuli, args.file, args.zoom, args.trigger, args.output_file)
    images.lancement()