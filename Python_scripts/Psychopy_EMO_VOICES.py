import csv
import os
import random
from datetime import datetime

import argparse
from psychopy import visual, event, core, sound
from Paradigme_parent import Parente


class voices(Parente):

    def __init__(self, duration, betweenstimuli, file, output, port, baudrate, trigger, activation, hauteur,
                 largeur, random, launching):
        self.win = visual.Window(size=(800, 600), fullscr=True)
        self.win.winHandle.activate()
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )
        event.globalKeys.add(key='escape', func=self.win.close)
        self.mouse = event.Mouse(win=self.win)
        self.file = file
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.output = output
        self.launching = launching
        self.timer = core.Clock()
        self.global_timer = core.Clock()
        self.voices=[]
        self.onset=[]
        self.duration=[]
        self.trial_type=[]
        self.stim_file=[]
        self.reaction = []
        self.port = port
        self.image_stim = visual.ImageStim(
            win=self.win,
            image="Input/Paradigme_EMO_VOICES/oreille.png",
            pos=(0, 0)
        )
        self.baudrate = baudrate
        self.trigger = trigger
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(self.output)
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random=False
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)

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
        texts = super().inputs_texts("Input/Paradigme_EMO_VOICES/"+self.launching)
        super().launching_texts(self.win, texts, self.trigger)
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'duration', 'trial_type', 'reaction','stim_file' ])
        self.voices = self.reading("Input/Paradigme_EMO_VOICES/"+self.file)
        if self.random:
            random.shuffle(self.voices)
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        for x in self.voices:
            custom_sound = sound.Sound("Input/Paradigme_EMO_VOICES/emo_voices/"+x)
            clicked = False
            clicked_time = "None"
            custom_sound.Sound= x
            self.timer.reset()
            self.cross_stim.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            while self.timer.getTime() < random.uniform(self.betweenstimuli-0.5,self.betweenstimuli+0.5):
                pass
            time_long = self.timer.getTime()
            trial_type = "Fixation"
            stim_file = "None"
            reaction = "None"
            super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), super().float_to_csv(time_long), trial_type, reaction, stim_file])

            self.image_stim.draw()
            self.rect.draw()
            self.timer.reset()
            self.win.flip()
            if self.activation:
                super().send_character(self.port,self.baudrate)
            custom_sound.play()
            onset = self.global_timer.getTime()
            while self.timer.getTime()<custom_sound.getDuration():
                button = self.mouse.getPressed()
                if any(button):
                    if not clicked:
                        clicked_time = self.timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True
            time_long = self.timer.getTime()
            trial_type = "Stimuli"
            stim_file = x
            reaction = clicked_time
            if reaction != "None":
                reaction = super().float_to_csv(reaction)
            super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), super().float_to_csv(time_long), trial_type, reaction, stim_file])
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
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)



    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()
    paradigm = voices(args.duration, args.betweenstimuli, args.file, args.output_file, args.port, args.baudrate,
                      args.trigger, args.activation, args.hauteur, args.largeur, args.random, args.launching)
    paradigm.lancement()

