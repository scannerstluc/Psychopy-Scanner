import csv
import os
from datetime import datetime

import argparse
from psychopy import visual, event, core, sound


class voices:

    def __init__(self, duration, betweenstimuli, file, output):
        self.win = visual.Window(fullscr=True)
        self.cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'
        )
        event.globalKeys.add(key='escape', func=self.win.close)
        self.mouse = event.Mouse(win=self.win)
        self.file = file
        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.output = output
        self.timer = core.Clock()
        self.global_timer = core.Clock()
        self.voices=[]
        self.onset=[]
        self.duration=[]
        self.trial_type=[]
        self.stim_file=[]
        self.reaction = []

    def reading(self,filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste


    def wait_for_trigger(self, port='COM3', baudrate=9600, trigger_char='s'):
        event.waitKeys()

    def write_tsv(self, onset, duration, file_stimuli, trial_type, reaction, filename="output.tsv"):
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
            tsv_writer.writerow(['onset', 'duration', 'trial_type', 'reaction','stim_file' ])
            for i in range(len(onset)):
                tsv_writer.writerow([onset[i], duration[i], trial_type[i], reaction[i], file_stimuli[i]])

    def lancement(self):
        self.voices = self.reading("Paradigme_EMO_VOICES/"+self.file)
        self.wait_for_trigger()
        for x in self.voices:
            custom_sound = sound.Sound("Paradigme_EMO_VOICES/emo_voices/"+x)
            clicked = False
            clicked_time = "None"
            custom_sound.Sound= x
            self.timer.reset()
            self.cross_stim.draw()
            self.win.flip()
            self.onset.append(self.global_timer.getTime())
            while self.timer.getTime() < self.betweenstimuli:
                pass
            self.duration.append(self.timer.getTime())
            self.trial_type.append("Fixation")
            self.stim_file.append("None")
            self.reaction.append("None")
            text_stim = visual.TextStim(self.win, wrapWidth=1.5, font="Arial", text="Audio")
            text_stim.draw()
            self.timer.reset()
            self.win.flip()
            custom_sound.play()
            self.onset.append(self.global_timer.getTime())
            while self.timer.getTime()<custom_sound.getDuration():
                button = self.mouse.getPressed()
                if any(button):
                    if not clicked:
                        clicked_time = self.timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True
            self.duration.append(self.timer.getTime())
            self.trial_type.append("Stimuli")
            self.stim_file.append(x)
            self.reaction.append(clicked_time)

        self.write_tsv(self.onset,self.duration,self.stim_file,self.trial_type,self.reaction,self.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=int, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=int, required=True, help="Temps entre les stimuli")

    args = parser.parse_args()
    paradigm = voices(args.duration, args.betweenstimuli, args.file, args.output_file)
    paradigm.lancement()

