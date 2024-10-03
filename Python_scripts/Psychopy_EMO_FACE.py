import csv
import os
import random
from datetime import datetime

import argparse
from psychopy import visual, event, core
from Paradigme_parent import Parente
from PIL import Image



class Emo_Face(Parente):


    def __init__(self, duration, betweenstimuli, filepath, output, port, baudrate, trigger, activation, hauteur,
                 largeur, zoom, random, launching):
        self.onset = []
        self.duration = []
        self.stimuli_file =[]
        self.trial_type = []
        self.click_times = []  # Pour stocker les temps de clic
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.filepath = filepath
        self.output= output
        self.port = port
        self.baudrate = baudrate
        self.zoom = zoom
        self.trigger = trigger
        self.launching = launching
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(self.output)
        self.win = visual.Window(size=(800, 600), fullscr=True, units="norm")
        self.win.winHandle.activate()
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random = False
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(win=self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)

    def redimension(self, hauteur, largeur):
        new_hauteur = (hauteur*self.zoom*4)+100
        new_largeur = (largeur*self.zoom*4)+100
        return new_hauteur,new_largeur
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
        self.mouse = event.Mouse(win=self.win)
        event.globalKeys.add(key='escape', func=self.win.close)
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'duration', 'trial_type', 'reaction','stim_file' ])

        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )

        images = []
        images_files = self.reading("Input/Paradigme_EMO_FACE/"+self.filepath)
        if self.random:
            random.shuffle(images_files)

        for image in images_files:
            image_stim = visual.ImageStim(
                win=self.win,
                pos=(0, 0),
                image = "Input/Paradigme_EMO_FACE/EMO_faces_list/"+image,
                size=None
            )
            base_width, base_height = image_stim.size  # Taille par défaut de l'image
            zoom_factor = 0.2+ (0.012 * self.zoom)  # Ajustement du facteur de zoom

            # Ajuster la taille en fonction du facteur de zoom
            image_stim.size = (base_width * zoom_factor, base_height * zoom_factor)
            images.append(image_stim)

        texts = super().inputs_texts("Input/Paradigme_EMO_FACE/"+self.launching)
        super().launching_texts(self.win, texts, self.trigger)
        super().wait_for_trigger(self.trigger)
        global_timer = core.Clock()
        timer = core.Clock()
        for image_stim in images:
            timer.reset()
            cross_stim.draw()
            self.win.flip()
            onset = global_timer.getTime()
            while timer.getTime() < random.uniform(self.betweenstimuli-0.5, self.betweenstimuli+0.5):
                pass
            long_time = timer.getTime()
            click_times = "None"
            stimuli_file = "None"
            trial_type = "Fixation"
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(long_time), trial_type, click_times, stimuli_file])
            clicked = False  # Variable pour vérifier si un clic a été détecté
            clicked_time = "None"
            timer.reset()
            image_stim.draw()
            self.rect.draw()
            self.win.flip()
            if self.activation:
                super().send_character(self.port,self.baudrate)
            onset = global_timer.getTime()
            while timer.getTime() < self.stimuli_duration:
                button = self.mouse.getPressed()  # Mise à jour de l'état des boutons de la souris
                if any(button):
                    if not clicked:  # Vérifier si c'est le premier clic détecté
                        clicked_time = timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True  # Empêcher l'enregistrement de clics multiple
            click_times = clicked_time
            long_time = timer.getTime()
            stimuli_file = image_stim.image[40:]
            trial_type = "Stimuli"
            if click_times != "None":
                click_times = super().float_to_csv(click_times)
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(long_time), trial_type, click_times, stimuli_file])

        super().the_end(self.win)
        self.win.close()
        core.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--zoom", type=float, required=True, help="Pourcentage Zoom")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)




    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")


    args = parser.parse_args()
    paradigm = Emo_Face(args.duration, args.betweenstimuli, args.file,
                        args.output_file, args.port, args.baudrate, args.trigger, args.activation,
                        args.hauteur, args.largeur, args.zoom, args.random, args.launching)
    paradigm.lancement()


