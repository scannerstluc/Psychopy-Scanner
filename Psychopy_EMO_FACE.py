import csv
import os
from datetime import datetime

from psychopy import visual, event, core



class Emo_Face:


    def __init__(self):
        self.onset = []
        self.duration = []
        self.stimuli_file =[]
        self.trial_type = []
        self.click_times = []  # Pour stocker les temps de clic

    def reading(self,filename):
        with open(filename, "r") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

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
        self.win = visual.Window(fullscr=False)
        self.mouse = event.Mouse(win=self.win)
        global_timer=core.Clock()
        timer = core.Clock()
        event.globalKeys.add(key='escape', func=self.win.close)

        Premier_texte = ("Dans l'exercice qui va suivre vous verrez apparaitre des adjectifs. \n" +
                                 "Suivant la consigne, vous devrez juger pour chaque adjectif: \n\n" +
                                 "-comment il s'applique à vous-même \n" +
                                 "-comment il s'applique à votre meilleur(e) ami(e) \n" +
                                 "-ou alors donner le nombre de syllabes qui le composent\n\n" +
                                 "(appuyer sur une touche pour lire la suite)")

        texte = visual.TextStim(self.win, text=Premier_texte, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font='Arial')
        texte.draw()
        self.win.flip()
        core.wait(3)

        images = []
        for image in self.reading("Paradigme_EMO_FACE/EMO_FACE_Chemin.txt"):
            image_stim = visual.ImageStim(
                win=self.win,
                pos=(0, 0),
                size=None
            )
            image = "Paradigme_EMO_FACE/EMO_faces_list/"+image
            image_stim.image=image
            images.append(image_stim)

        for image_stim in images:
            image_stim.draw()
            self.win.flip()
            self.onset.append(global_timer.getTime())
            timer.reset()

            clicked = False  # Variable pour vérifier si un clic a été détecté
            clicked_time = "None"
            while timer.getTime() < 3:
                button = self.mouse.getPressed()  # Mise à jour de l'état des boutons de la souris

                if any(button):
                    if not clicked:  # Vérifier si c'est le premier clic détecté
                        clicked_time = timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True  # Empêcher l'enregistrement de clics multiples

                # Vous pouvez ajouter ici d'autres actions à exécuter pendant l'attente
            self.click_times.append(clicked_time)
            self.duration.append(timer.getTime())
            self.stimuli_file.append(image_stim.image[34:])
            self.trial_type.append("stimuli")

        print(self.onset)
        print(self.duration)
        print(self.stimuli_file)
        print(self.trial_type)
        print(self.click_times)

        self.write_tsv(self.onset,self.duration,self.stimuli_file,self.trial_type, self.click_times,"montesttttttt")
        self.win.close()
        core.quit()

Emo_Face().lancement()
