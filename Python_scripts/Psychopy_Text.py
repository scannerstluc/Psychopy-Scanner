import argparse
import os
from datetime import datetime

import serial
from psychopy import visual, core, event
import csv
from Paradigme_parent import Parente


class PsychoPyParadigm(Parente):
    def __init__(self, duration, words, zoom, file, output, port, baudrate, trigger, activation):
        self.duration = int(duration)
        self.words = words
        self.zoom = zoom
        self.file = file
        self.stimuli_times = []
        self.stimuli_apparition = []
        self.stimuli = []
        self.global_timer= core.Clock()
        self.output=output
        self.port = port
        self.baudrate = baudrate
        self.trigger = trigger
        if activation == "True":
            self.activation = True
        else:
            self.activation = False


    def affichage_mots(self, win, text_stim, words, display_time):
        timer = core.Clock()
        for word in words:
            text_stim.setText(word)
            text_stim.draw()
            win.flip()
            if self.activation and words != [":; $+", " #^=-", ":?$µ", "###"]:
                super().send_character(self.port,self.baudrate)
            self.stimuli_apparition.append(self.global_timer.getTime())  # Enregistrer le moment où le stimulus apparaît
            timer.reset()  # Réinitialiser l'horloge à chaque nouveau mot
            while timer.getTime() < display_time:
                pass  # Attendre sans bloquer d'autres processus
            self.stimuli_times.append(timer.getTime())
            self.stimuli.append(word)

    def reading(self, filename):
        filename = "Input/Paradigme_mots/" + filename
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

    def pause_for_seconds(self, seconds):
        timer = core.Clock()
        timer.reset()
        while timer.getTime() < seconds:
            pass

    def words_psychopy(self):
        win = visual.Window(fullscr=True, color=[-1, -1, -1], units='pix')
        event.globalKeys.add(key='escape', func=win.close)

        text_stim = visual.TextStim(win, text='', color=[1, 1, 1], height=90+(90*self.zoom/100))

        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        nothinkinglist = [":; $+", " #^=-", ":?$µ", "###"]
        self.affichage_mots(win, text_stim, nothinkinglist, self.duration)
        self.affichage_mots(win, text_stim, self.words, self.duration)
        self.affichage_mots(win, text_stim, nothinkinglist, self.duration)
        self.pause_for_seconds(3)  # Pause de 5 secondes avant de fermer

        win.close()

    def pas_un_stimuli(self, stimuli):
        alphabet = ";:/.,?#@&|£$[]=~"
        for char in alphabet:
            if char in stimuli:
                return True
        return False
    def write_tsv(self, filename="output1.tsv"):
        filename = super().preprocessing_tsv(filename)

        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['onset', 'duration', 'stimuli', 'trial_type'])
            type_stimuli = []
            for x in range(len(self.stimuli)):
                if self.pas_un_stimuli(self.stimuli[x]):
                    type_stimuli.append("Noise")
                else:
                    type_stimuli.append("Stimuli")
            for i in range(len(self.stimuli_apparition)):
                tsv_writer.writerow([self.stimuli_apparition[i], self.stimuli_times[i], self.stimuli[i], type_stimuli[i]])

    def run(self):
        if self.file:
            self.words = self.reading(self.file)
        else:
            self.words = [word.strip() for word in self.words.split(',')]
        self.words_psychopy()
        self.write_tsv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--words", type=str, required=True, help="Liste de mots pour le paradigme")
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")

    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")

    args = parser.parse_args()
    paradigm = PsychoPyParadigm(args.duration, args.words, args.zoom, args.file,args.output_file,args.port,
                                args.baudrate, args.trigger, args.activation)
    paradigm.run()
