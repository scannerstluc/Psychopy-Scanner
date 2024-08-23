import csv
import os
from datetime import datetime

import argparse
from psychopy import visual, event, core
from Paradigme_parent import Parente



class Emo_Face(Parente):


    def __init__(self, duration, betweenstimuli, filepath, output):
        self.onset = []
        self.duration = []
        self.stimuli_file =[]
        self.trial_type = []
        self.click_times = []  # Pour stocker les temps de clic
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.filepath = filepath
        self.output= output

    def reading(self,filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

    def write_tsv(self, onset, duration, file_stimuli, trial_type, reaction, filename="output.tsv"):
        filename = super().preprocessing_tsv(filename)

        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['onset', 'duration', 'trial_type', 'reaction','stim_file' ])
            for i in range(len(onset)):
                tsv_writer.writerow([onset[i], duration[i], trial_type[i], reaction[i], file_stimuli[i]])

    def lancement(self):
        self.win = visual.Window(fullscr=True)
        self.mouse = event.Mouse(win=self.win)
        global_timer=core.Clock()
        timer = core.Clock()
        event.globalKeys.add(key='escape', func=self.win.close)

        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )

        images = []
        for image in self.reading("Input/Paradigme_EMO_FACE/"+self.filepath):
            image_stim = visual.ImageStim(
                win=self.win,
                pos=(0, 0),
                size=None
            )
            image = "Input/Paradigme_EMO_FACE/EMO_faces_list/"+image
            image_stim.image=image
            images.append(image_stim)

        super().wait_for_trigger("s")
        for image_stim in images:
            timer.reset()
            cross_stim.draw()
            self.win.flip()
            self.onset.append(global_timer.getTime())

            while timer.getTime() < self.betweenstimuli:
                pass
            self.duration.append(timer.getTime())
            self.click_times.append("None")
            self.stimuli_file.append("None")
            self.trial_type.append("Fixation")
            clicked = False  # Variable pour vérifier si un clic a été détecté
            clicked_time = "None"
            timer.reset()
            image_stim.draw()
            self.win.flip()
            self.onset.append(global_timer.getTime())
            while timer.getTime() < self.stimuli_duration:
                button = self.mouse.getPressed()  # Mise à jour de l'état des boutons de la souris

                if any(button):
                    if not clicked:  # Vérifier si c'est le premier clic détecté
                        clicked_time = timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True  # Empêcher l'enregistrement de clics multiple

                # Vous pouvez ajouter ici d'autres actions à exécuter pendant l'attente
            self.click_times.append(clicked_time)
            self.duration.append(timer.getTime())
            self.stimuli_file.append(image_stim.image[40:])
            self.trial_type.append("stimuli")


        self.write_tsv(self.onset,self.duration,self.stimuli_file,self.trial_type, self.click_times,self.output)
        self.win.close()
        core.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")


    args = parser.parse_args()
    paradigm = Emo_Face(args.duration, args.betweenstimuli, args.file, args.output_file)
    paradigm.lancement()


