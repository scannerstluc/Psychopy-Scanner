import argparse
import csv
import os
from collections import defaultdict
from datetime import datetime
import random

from psychopy import visual, core, event
import serial


class Localizer:
    def __init__(self, duration, betweenstimuli, number_of_block, number_per_block, port, baudrate, trigger,  output):
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
        self.port= port
        self.baudrate = baudrate
        self.trigger = trigger
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
    def lancement(self):
        self.wait_for_trigger(self.port, self.baudrate, self.trigger)
        for x in range (self.number_of_blocks):
            self.show_block(random.choice(self.keys),2)
        self.write_tsv(self.onset,self.duration,self.block_type, self.stim_file, self.trial_type,self.output)

    def wait_for_trigger(self, port='COM3', baudrate=9600, trigger_char='s'):
        with serial.Serial(port, baudrate=baudrate) as ser:
            trigger = ser.read().decode('utf-8')
            while trigger != trigger_char:
                trigger = ser.read().decode('utf-8')
            print("Trigger received")

    def write_tsv(self, onset, duration, block_type, file_stimuli, trial_type, filename="output.tsv"):
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
            tsv_writer.writerow(['onset', 'duration', "block_type" ,'stim_file','trial_type' ])
            for i in range(len(onset)):
                tsv_writer.writerow([onset[i], duration[i], block_type[i], file_stimuli[i], trial_type[i]])
    def get_groups_and_keys(self):
        import os
        directory_path = 'Paradigme_LOCALIZER/images'
        for filename in os.listdir(directory_path):
            if filename.endswith((".jpg", ".jpeg")):
                prefix = ''.join([char for char in filename if not char.isdigit()]).rstrip('_')
                self.groups[prefix].append(filename)
                self.groups[prefix+"1"].append(filename)
        for key in self.groups.keys():
            self.keys.append(key)


    def show_block(self, group_name, number_per_block):
        toshow=[]
        while len(toshow)<number_per_block:
            if self.groups[group_name] != []:
                stimuli=random.choice(self.groups[group_name])
                self.groups[group_name].remove(stimuli)
                toshow.append(stimuli)
            else:
                stimuli=random.choice(self.groups[group_name+"1"])
                toshow.append(stimuli)
        liste_image_win=[]
        for image in toshow:
            image_path = "Paradigme_LOCALIZER/images/" + image
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
            self.win.flip()
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
    parser.add_argument("--duration", type=int, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--blocks", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--per_block", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=int, required=True, help="Temps entre les stimuli")
    parser.add_argument('--port', type=str, required=True, help="Port")
    parser.add_argument('--baudrate', type=int, required=True, help="Speed port")
    parser.add_argument('--trigger', type=str, required=True, help="caractère pour lancer le programme")
    args = parser.parse_args()

    localizer = Localizer(args.duration,args.betweenstimuli,args.blocks,args.per_block, args.port, args.baudrate, args.trigger, args.output_file)
    localizer.lancement()
