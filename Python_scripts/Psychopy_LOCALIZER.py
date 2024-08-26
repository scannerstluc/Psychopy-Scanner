import argparse
import csv
import os
from collections import defaultdict
from datetime import datetime
import random

from psychopy import visual, core, event
import serial
from Paradigme_parent import Parente



class Localizer(Parente):
    def __init__(self, duration, betweenstimuli, number_of_block, number_per_block, output, port, baudrate, trigger,
                 activation, hauteur, largeur, random):
        self.win = visual.Window(size=(800, 600), fullscr=True)
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        event.globalKeys.add(key='escape', func=self.win.close)
        self.timer = core.Clock()
        self.global_timer = core.Clock()
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.number_of_blocks = number_of_block
        self.number_per_block = number_per_block
        self.output = output
        self.voices = []
        self.onset = []
        self.duration = []
        self.trial_type = []
        self.stim_file = []
        self.groups = defaultdict(list)
        self.keys = []
        self.block_type = []
        self.get_groups_and_keys()
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

        self.ordre=self.reading("Input/Paradigme_LOCALIZER/block_order.txt")
        print(self.activation)
        print(self.ordre)
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)

    def lancement(self):
        super().wait_for_trigger(self.trigger)
        for x in range (self.number_of_blocks):
            if self.random:
                self.show_block(random.choice(self.keys),self.number_per_block)
            else:
                y = x%8
                self.show_block(self.ordre[y],self.number_per_block)

        self.write_tsv(self.onset,self.duration,self.block_type, self.stim_file, self.trial_type,self.output)

    def reading(self,filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste
    def write_tsv(self, onset, duration, block_type, file_stimuli, trial_type, filename="output.tsv"):
        filename=super().preprocessing_tsv(filename)

        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['onset', 'duration', "block_type" ,'stim_file','trial_type' ])
            for i in range(len(onset)):
                tsv_writer.writerow([onset[i], duration[i], block_type[i], file_stimuli[i], trial_type[i]])
    def get_groups_and_keys(self):
        import os
        print("Getting groups and keys...")
        directory_path = 'Input/Paradigme_LOCALIZER/images'
        for filename in os.listdir(directory_path):
            if filename.endswith((".jpg", ".jpeg")):
                prefix = ''.join([char for char in filename if not char.isdigit()]).rstrip('_')
                self.groups[prefix].append(filename)
                self.groups[prefix+"1"].append(filename)
        for key in self.groups.keys():
            self.keys.append(key)
        print(self.keys)


    def show_block(self, group_name, number_per_block):
        toshow=[]
        while len(toshow)<number_per_block:
            if self.groups[group_name] != []:
                if self.random:
                    stimuli=random.choice(self.groups[group_name])
                else:
                    stimuli=self.groups[group_name][0]
                self.groups[group_name].remove(stimuli)
                toshow.append(stimuli)
            else:
                if self.random:
                    stimuli=random.choice(self.groups[group_name+"1"])
                else:
                    print(group_name)
                    stimuli=self.groups[group_name+"1"]
                toshow.append(stimuli)
        liste_image_win=[]
        for image in toshow:
            image_path = "Input/Paradigme_LOCALIZER/images/" + image
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0),
                size=None
            )
            #image_stim.size= 0.8+(0.3*self.zoom/100)
            liste_image_win.append(image_stim)
        count=0
        for image_stim in liste_image_win:
            self.onset.append(self.global_timer.getTime())
            self.cross_stim.draw()
            self.win.flip()
            self.timer.reset()  # Réinitialiser le timer à chaque nouvelle image
            while self.timer.getTime() < self.betweenstimuli:
                pass
            self.duration.append(self.timer.getTime())
            self.trial_type.append("Fixation")
            self.stim_file.append("None")
            self.block_type.append("None")
            self.onset.append(self.global_timer.getTime())
            image_stim.draw()
            self.rect.draw()
            self.win.flip()
            if self.activation:
                super().send_character(self.port,self.baudrate)
            self.timer.reset()  # Réinitialiser le timer à chaque nouvelle image
            while self.timer.getTime() < self.stimuli_duration:
                pass
            self.duration.append(self.timer.getTime())
            self.trial_type.append("Stimuli")
            self.stim_file.append(toshow[count])
            self.block_type.append(group_name)
            count+=1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--blocks", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--per_block", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")

    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()

    localizer = Localizer(args.duration,args.betweenstimuli,args.blocks,args.per_block, args.output_file,
                          args.port, args.baudrate, args.trigger, args.activation,
                         args.hauteur, args.largeur, args.random)
    localizer.lancement()
