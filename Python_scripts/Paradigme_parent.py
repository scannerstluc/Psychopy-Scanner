import csv
import os
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime
from psychopy import event, visual, core

import serial


class Parente(ABC):
    def preprocessing_tsv_csv(self, filename):
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
        filename_csv = os.path.join(output_dir, f"{filename_prefix}_csv_run{run_number}.csv")
        return filename, filename_csv

    def preprocessing_tsv(self, filename):
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
        return filename

    def inputs_texts(self,chemin):
        with open(chemin, 'r', encoding='utf-8') as file:
            contenu = file.read()
        texts = re.findall(r'\*(.*?)\*', contenu, re.DOTALL)
        return texts

    def wait_for_trigger(self, trigger='s'):
        event.waitKeys(keyList=[trigger])

    def proper_waitkey(self, trigger='s'):
        donottake = trigger
        while True:
            keys = event.waitKeys()
            if donottake not in keys:  # Condition pour quitter la boucle
                break

    def launching_texts(self,win,textes,trigger):
        y=0
        for x in range (len(textes)-1):
            self.Premier_texte = textes[x]
            texte = visual.TextStim(win, text=self.Premier_texte, color=[1, 1, 1], alignText="left", wrapWidth=1.5,
                                    font='Arial')
            texte.draw()
            win.flip()
            self.proper_waitkey(trigger)
            y=x+1
        text_after= visual.TextStim(win, text=textes[y], alignText="center", wrapWidth=1.5, font="Arial")
        text_after.draw()
        win.flip()

    def the_end (self, win):
        texte = visual.TextStim(win, text="End/Fin/Ende", color=[1, 1, 1], alignText="center", wrapWidth=1.5, font='Arial')
        texte.draw()
        win.flip()
        core.wait(4)
    def send_character(self, port, baud_rate):
        char = "t"
        try:
            # Ouvrir le port série
            with serial.Serial(port=port, baudrate=baud_rate, timeout=1) as ser:
                print(f"Connexion ouverte sur {port}. Envoi de '{char}'...")
                ser.write(b'H')
                time.sleep(0.5)
                ser.write(b'L')
                print("Pin 2 activé puis désactivé")  # Message de confirmation


        except serial.SerialException as e:
            print(f"Erreur d'ouverture ou d'utilisation du port série : {e}")

    def file_init(self, filename, filename_csv, columns):
        with open(filename, mode='w', newline='') as file1:
            csv_writer = csv.writer(file1, delimiter='\t')
            csv_writer.writerow(columns)

        with open(filename_csv, mode='w', newline='') as file1:
            csv_writer = csv.writer(file1, delimiter='\t')
            csv_writer.writerow(columns)

    def write_tsv_csv(self, filename, filename_csv, rows):
        with open(filename, mode='a', newline='') as file1:
            csv_writer = csv.writer(file1, delimiter='\t')
            csv_writer.writerow(rows)

        with open(filename_csv, mode='a', newline='') as file1:
            csv_writer = csv.writer(file1, delimiter='\t')
            csv_writer.writerow(rows)