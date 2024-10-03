import argparse
import copy
import csv
import os
from collections import defaultdict
from datetime import datetime
import random

from psychopy import visual, core, event
import serial
from Paradigme_parent import Parente



class Priming(Parente):
    def __init__(self, duration, betweenstimuli, betweenblocks, number_of_block, output, port, baudrate, trigger,
                 activation, hauteur, largeur, random, zoom, launching, file):
        self.win = visual.Window(size=(800, 600), fullscr=True, units="norm")
        self.win.winHandle.activate()
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        self.mouse = event.Mouse(win=self.win)
        event.globalKeys.add(key='escape', func=self.win.close)
        self.timer = core.Clock()
        self.global_timer = core.Clock()
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.number_of_blocks = number_of_block
        self.betweenblocks= betweenblocks
        self.output = output
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(self.output)
        self.launching = launching
        self.zoom = zoom
        self.file = file
        self.click_times = []
        self.voices = []
        self.onset = []
        self.duration = []
        self.trial_type = []
        self.stim_file = []
        self.keys = []
        self.block_type = []
        self.port = port
        self.baudrate = baudrate
        self.trigger = trigger
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random = False

        self.ordre=self.reading("Input/Paradigme_Priming/"+self.file)
        self.real_groups = self.real_reading("Input/Paradigme_Priming/" + self.file)
        self.copy_real_groups = copy.deepcopy(self.real_groups)
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)
    def real_reading(self,filename):
        with open(filename, 'r') as fichier:
            lignes = fichier.readlines()
        lignes = [ligne.strip() for ligne in lignes]
        groupes = []
        groupe_actuel = []

        for ligne in lignes:
            if ligne:
                groupe_actuel.append(ligne)
            else:
                if groupe_actuel:
                    groupes.append(groupe_actuel)
                    groupe_actuel = []
        if groupe_actuel:
            groupes.append(groupe_actuel)
        return groupes
    def lancement(self):
        texts = super().inputs_texts("Input/Paradigme_Priming/" + self.launching)
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'duration', "reaction", "block_index" ,'stim_file','trial_type' ])
        super().launching_texts(self.win, texts, self.trigger)
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        index_of_groups = len(self.real_groups) - 1
        for x in range (self.number_of_blocks):
            self.cross_stim.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            self.timer.reset()
            while self.timer.getTime() < self.betweenblocks:
                pass
            time_long = self.timer.getTime()
            The_None = "None"
            trial_type = "Fixation"
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(time_long), The_None, The_None, The_None, trial_type])
            if self.random:
                self.show_block(random.randint(0,index_of_groups),2)
            else:
                y = x % index_of_groups
                self.show_block(y, 2)
        super().the_end(self.win)

    def reading(self,filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste
    def write_tsv(self, onset, duration, block_type, file_stimuli, trial_type, filename="output.tsv"):
        filename=super().preprocessing_tsv(filename)

        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['onset', 'duration', "reaction", "block_index" ,'stim_file','trial_type' ])
            for i in range(len(onset)):
                tsv_writer.writerow([onset[i], duration[i], self.click_times[i], block_type[i], file_stimuli[i], trial_type[i]])


    def show_block(self, index, number_per_block):
        toshow=[]
        while len(toshow)<number_per_block:
            if self.real_groups[index] != []:
                if self.random:
                    stimuli = random.choice(self.real_groups[index])
                else:
                    stimuli = self.real_groups[index][0]
                self.real_groups[index].remove(stimuli)
                toshow.append(stimuli)
            else:
                if self.random:
                    stimuli = random.choice(self.copy_real_groups[index])
                else:
                    stimuli = self.copy_real_groups[index]
                toshow.append(stimuli)
        liste_image_win=[]
        for image in toshow:
            image_path = "Input/Paradigme_priming/stim_static/" + image
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0),
                size=None
            )
            base_width, base_height = image_stim.size
            zoom = 0.5 + (0.012 * self.zoom)
            image_stim.size = (base_width * zoom, base_height * zoom)
            liste_image_win.append(image_stim)
        count=0
        limite = len(liste_image_win)
        for image_stim in liste_image_win:
            onset = self.global_timer.getTime()
            image_stim.draw()
            self.rect.draw()
            self.win.flip()
            clicked = False  # Variable pour vérifier si un clic a été détecté
            clicked_time = "None"
            if self.activation:
                super().send_character(self.port,self.baudrate)
            self.timer.reset()  # Réinitialiser le timer à chaque nouvelle image
            while self.timer.getTime() < self.stimuli_duration:
                button = self.mouse.getPressed()  # Mise à jour de l'état des boutons de la souris
                if any(button):
                    if not clicked:  # Vérifier si c'est le premier clic détecté
                        clicked_time = self.timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True
            click_times = clicked_time
            time_long = self.timer.getTime()
            trial_type = "Stimuli"
            stim_file = toshow[count]
            block_type = index+1
            if click_times != "None":
                click_times = super().float_to_csv(click_times)
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(time_long), click_times, block_type, stim_file, trial_type])
            if count != limite-1:
                onset = self.global_timer.getTime()
                self.cross_stim.draw()
                self.win.flip()
                self.timer.reset()  # Réinitialiser le timer à chaque nouvelle image
                while self.timer.getTime() < self.betweenstimuli:
                    pass
                time_long = self.timer.getTime()
                The_None = "None"
                trial_type = "Fixation"
                super().write_tsv_csv(self.filename, self.filename_csv,
                                      [super().float_to_csv(onset), super().float_to_csv(time_long), The_None, The_None, The_None, trial_type])
            count+=1

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--blocks", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--zoom", type=float, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")
    parser.add_argument("--betweenblocks", type=float, required=True, help="Temps entre les blocks")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--file", type=str, required=True, help="Nom du fichier d'input")



    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()

    prime = Priming(args.duration,args.betweenstimuli, args.betweenblocks, args.blocks, args.output_file,
                          args.port, args.baudrate, args.trigger, args.activation,
                         args.hauteur, args.largeur, args.random, args.zoom, args.launching, args.file)
    prime.lancement()
