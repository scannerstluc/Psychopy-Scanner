import csv
import os
from datetime import datetime

import argparse
import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
from psychopy import visual, core, event
from Paradigme_parent import Parente


class Colors(Parente):
    def __init__(self, duration, betweenstimuli, zoom, langage, filepath, output):
        self.win = visual.Window(fullscr=True, color="black")
        event.globalKeys.add(key='escape', func=self.win.close)
        self.fs = 44100  # fréquence d'échantillonnage
        self.stimuli_duration = duration  # durée de l'enregistrement en secondes
        self.betweenstimuli = betweenstimuli
        self.zoom = zoom
        self.filepath = filepath
        self.output = output
        self.threshold = 1000  # seuil pour détecter le début de la parole (à ajuster selon votre micro/environnement)
        self.timer = core.Clock()  # création de l'horloge
        self.global_timer = core.Clock()
        self.patient_id = output
        self.onset = []
        self.duration = []
        self.stimuli = []
        self.trial_type= []
        self.reaction = []
        self.langue = langage


        self.cross_stim = visual.ShapeStim(
                win=self.win,
                vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
                lineWidth=3,
                closeShape=False,
                lineColor="white",
                units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
            )

    def reading(self,filename):
        words = []
        colors = []
        stimuli = []
        with open(filename, "r", encoding="utf-8") as fichier:
            for line in fichier:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    words.append(parts[0].strip())
                    colors.append(parts[1].strip())
        for x in range(len(words)):
            mot = words[x]+"_"+colors[x]
            stimuli.append(mot)
        return words, colors, stimuli

    def reconnaissance(self,chemin):
        recognizer = sr.Recognizer()

        audio_file = chemin

        # Utiliser SpeechRecognition pour convertir l'audio en texte
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                if self.langue == "Francais":
                    text = recognizer.recognize_google(audio_data, language="fr-FR")
                elif self.langue == "Anglais":
                    text = recognizer.recognize_google(audio_data, language="en-US")
                elif self.langue == "Dannois":
                    text = recognizer.recognize_google(audio_data, language="da-DK")
                return text
            except sr.UnknownValueError:
                return "None/pas reconnu"
                print("Google Speech Recognition n'a pas pu comprendre l'audio")
            except sr.RequestError as e:
                return "None/pas reconnu"
                print(f"Erreur lors de la demande à Google Speech Recognition; {e}")

    def write_tsv(self,onset, duration,stimuli, trial_type, recording, reaction_time, filename="output.tsv"):
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
        dirname = os.path.join(output_dir, f"{filename_prefix}_run{run_number}")
        os.makedirs(dirname, exist_ok=True)
        for i in range (len(recording)):
            record = os.path.join(dirname, f"record{i}.wav")
            sf.write(record, recording[i], self.fs)
        special_count=0
        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['onset', 'duration', 'stimuli', 'trial_type', 'response','time_before_starting_to_answer', ])
            for i in range(len(onset)):
                if i%2!=0:
                    tsv_writer.writerow([onset[i], duration[i],stimuli[i], trial_type[i], self.reconnaissance(dirname+"/record"+str(special_count)+".wav"), reaction_time[i] ])
                    special_count+=1
                else:
                    tsv_writer.writerow([onset[i], duration[i],stimuli[i], trial_type[i], "None",reaction_time[i] ])


    def lancement(self):
        words, colors, stimuli_names=self.reading("Input/Paradigme_Couleur/"+self.filepath)
        text_stim = visual.TextStim(self.win, wrapWidth=1.5, font="Arial", height=0.1+(0.01*self.zoom))
        count=0
        super().wait_for_trigger("s")
        self.global_timer.reset()
        recordings=[]
        for mot in words:
            self.cross_stim.draw()
            self.win.flip()
            self.onset.append(self.global_timer.getTime())
            self.timer.reset()
            while self.timer.getTime() < self.betweenstimuli:
                pass
            self.duration.append(self.timer.getTime())
            self.stimuli.append("Cross")
            self.reaction.append("None")
            self.trial_type.append("Fixation")
            text_stim.text=mot
            text_stim.color=colors[count]
            text_stim.draw()
            self.win.flip()
            self.onset.append(self.global_timer.getTime())
            self.timer.reset()
            recording = sd.rec(int(self.stimuli_duration * self.fs), samplerate=self.fs, channels=1, dtype='int16')
            sd.wait()
            self.duration.append(self.timer.getTime())
            self.stimuli.append(stimuli_names[count])
            self.trial_type.append("Stimuli")
            start_time = None
            for i, sample in enumerate(recording):
                if np.abs(sample) > self.threshold:
                    start_time = i / self.fs
                    break
            if start_time is not None:
                print(f"L'utilisateur a commencé à parler à {start_time:.2f} secondes.")
            else:
                start_time="None"
                print("Aucune parole détectée.")
            self.reaction.append(start_time)
            count+=1
            recordings.append(recording)
        self.write_tsv(self.onset,self.duration, self.stimuli,self.trial_type, recordings, self.reaction, self.patient_id)
        self.win.close()
        core.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--zoom", type=int, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Temps entre les stimuli")
    parser.add_argument("--choice", type=str, required=True, help="Choix de la langue")

    args = parser.parse_args()
    colors = Colors(args.duration, args.betweenstimuli, args.zoom, args.choice, args.file, args.output_file).lancement()


#Colors(duration=2,betweenstimuli=1,zoom=10,filepath="colors_list.txt", output="wififi").lancement()