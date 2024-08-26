import argparse
import copy
import csv
import os
from datetime import datetime

from psychopy import visual, core, event
import serial
from Paradigme_parent import Parente


class VideoPsycho(Parente):
    def __init__(self, duration, betweenstimuli, file, zoom, output, port, baudrate, trigger, activation):
        self.duration = duration
        self.betweenstimuli = betweenstimuli
        self.file = file
        self.zoom = zoom
        self.output = output
        self.port = port
        self.baudrate = baudrate
        self.trigger = trigger
        if activation == "True":
            self.activation = True
        else:
            self.activation = False


    def reading(self, filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste


    def play_video_psychopy(self, chemin, duration, between_stimuli, zoom, trigger):
        apparition_stimuli = []
        longueur_stimuli = []
        stimuli_liste = []
        videos = self.reading(chemin)
        file = copy.copy(videos)
        for x in range(len(videos)):
            videos[x] = "Input/Paradigme_video/Stimuli/" + videos[x]
        win = visual.Window(
            fullscr=True,
            #color = [0, 0, 1],
            #color = [1,0,0],
            color= [-0.042607843137254943, 0.0005215686274509665, -0.025607843137254943],
            units="pix"
        )
        event.globalKeys.add(key='escape', func=win.close)

        cross_stim = visual.ShapeStim(
            win=win,
            vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
            lineWidth=3,
            closeShape=False,
            lineColor="white"
        )
        super().wait_for_trigger(self.trigger)
        global_timer = core.Clock()
        thezoom = 1.3+(0.77*zoom/100)
        for x in range(len(videos)):
            timer = core.Clock()
            video_path = videos[x]
            movie_stim = visual.MovieStim(
                win=win,
                filename=video_path,
                size=[1920,1080],
                pos=(0, 0),
                opacity=1.0,
                flipVert=False,
                flipHoriz=False,
                loop=True,
                units='norm'
            )
            cross_stim.draw()
            win.flip()
            timer.reset()
            apparition_stimuli.append(global_timer.getTime())
            while timer.getTime() < between_stimuli:
                pass
            longueur_stimuli.append(timer.getTime())
            stimuli_liste.append("Fixation")
            movie_stim.size = thezoom
            timer.reset()
            apparition_stimuli.append(global_timer.getTime())
            if self.activation:
                super().send_character(self.port,self.baudrate)
            while timer.getTime() < duration:
                movie_stim.draw()
                win.flip()
            longueur_stimuli.append(timer.getTime())
            stimuli_liste.append(file[x])

        cross_stim.draw()
        win.flip()
        timer.reset()
        apparition_stimuli.append(global_timer.getTime())
        while timer.getTime() < between_stimuli:
            pass
        longueur_stimuli.append(timer.getTime())
        stimuli_liste.append("Fixation")
        win.close()
        return longueur_stimuli, apparition_stimuli, stimuli_liste

    def write_tsv(self, onset, duration, file_stimuli, trial_type, filename="output.tsv"):
        filename = super().preprocessing_tsv(filename)


        with open(filename, mode='w', newline='') as file:
                tsv_writer = csv.writer(file, delimiter='\t')
                tsv_writer.writerow(['onset', 'duration', 'trial_type', 'stim_file'])
                for i in range(len(onset)):
                    tsv_writer.writerow([onset[i], duration[i], trial_type[i], file_stimuli[i]])


    def lancement(self):

        stimulus_times, stimulus_apparition, stimuli = self.play_video_psychopy(self.file, self.duration, self.betweenstimuli, self.zoom, self.trigger)
        liste_trial = []
        liste_lm = []
        count = 0
        for x in stimuli:
            if x == "Fixation":
                liste_lm.append(count)
                liste_trial.append("Fixation")
            else:
                liste_trial.append("Stimuli")
            count += 1
        for x in liste_lm:
            stimuli[x] = "None"
        self.write_tsv(stimulus_apparition, stimulus_times, stimuli, liste_trial, self.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")

    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")

    args = parser.parse_args()
    videos= VideoPsycho(args.duration, args.betweenstimuli, "Input/Paradigme_video/"+args.file, args.zoom,
                         args.output_file, args.port, args.baudrate, args.trigger, args.activation)
    videos.lancement()