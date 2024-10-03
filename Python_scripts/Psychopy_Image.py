import argparse
import csv
import os
import random
from datetime import datetime

from Paradigme_parent import Parente
from psychopy import visual, core, event
import serial



class static_image(Parente):
    def __init__(self, duration, betweenstimuli, file, zoom, output, port, baudrate, trigger, activation, hauteur,
                 largeur, random, launching):
        self.duration = duration #args.duration, args.betweenstimuli, args.file, args.zoom, args.port, args.baudrate, args.trigger  ,args.output_file)
        self.betweenstimuli = betweenstimuli
        self.file = file
        self.zoom = zoom
        self.click_times = []
        self.win = visual.Window(size=(800, 600), fullscr=True, units="norm")
        self.win.winHandle.activate()
        self.mouse = event.Mouse(win=self.win)
        event.globalKeys.add(key='escape', func=self.win.close)
        self.output = output
        self.filename, self.filename_csv = super().preprocessing_tsv_csv(output)
        self.port = port
        self.global_timer = core.Clock() #Horloge principale
        self.baudrate = baudrate
        self.trigger = trigger
        self.launching = launching
        if activation == "True":
            self.activation = True
        else:
            self.activation = False
        if random == "True":
            self.random = True
        else:
            self.random = False
        rect_width = largeur
        rect_height = hauteur
        self.rect = visual.Rect(self.win, width=rect_width, height=rect_height, fillColor='white', lineColor='white',
                                units='pix')
        self.rect.pos = (self.win.size[0] / 2 - rect_width / 2, self.win.size[1] / 2 - rect_height / 2)



    def reading(self, filename):
        filenames = []
        angles = []
        with open(filename, "r") as fichier:
            for line in fichier:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    filenames.append(parts[0].strip())
                    angles.append(int(parts[1].strip()))
        return filenames, angles

    def static_images_psychopy(self, chemin, duration, betweenstimuli):
        chemin = "Input/Paradigme_images_statiques/" + chemin
        images, orientation = self.reading(chemin)
        super().file_init(self.filename, self.filename_csv,
                          ['onset', 'duration', 'trial_type', 'angle', 'reaction', 'stim_file'])
        if self.random:
            combined = list(zip(images, orientation))
            random.shuffle(combined)
            liste1_mixed, liste2_mixed = zip(*combined)
            images = list(liste1_mixed)
            orientation = list(liste2_mixed)
        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )
        thezoom = 0.7 + (0.012*self.zoom)
        #thezoom = 1 if zoom else 0.5
        timer = core.Clock()  # Horloge réinitialisée à chaque stimuli
        stimulus_times = []  # Liste pour enregistrer la durée des stimuli
        stimulus_apparition=[] #Liste pour enregistrer le timing d'apparition des stimuli
        stimuli_liste = [] #Liste pour enregistrer les noms des stimuli, si c'est une croix ce sera Fixation sinon le nom du fichier
        liste_image_win = []
        count = 0
        for image in images:
            image_path = "Input/Paradigme_images_statiques/stim_static/" + image
            image_stim = visual.ImageStim(
                win=self.win,
                image=image_path,
                pos=(0, 0)
            )

            base_width, base_height = image_stim.size  # Taille par défaut de l'image
            zoom_factor = 0.5 + (0.012 * self.zoom)  # Ajustement du facteur de zoom

            # Ajuster la taille en fonction du facteur de zoom
            image_stim.size = (base_width * zoom_factor, base_height * zoom_factor)
            image_stim.ori = orientation[count]  # Orientation de l'image
            liste_image_win.append(image_stim)
            stimuli_liste.append(image)
            stimuli_liste.append("Fixation")
            count += 1

        texts = super().inputs_texts("Input/Paradigme_images_statiques/"+self.launching)
        super().launching_texts(self.win, texts,self.trigger)
        super().wait_for_trigger(self.trigger)
        self.global_timer.reset()
        cross_stim.draw()
        self.win.flip()
        timer.reset()
        onset = self.global_timer.getTime()
        while timer.getTime() < random.uniform(betweenstimuli-0.5,betweenstimuli+0.5):
            pass
        time_long = timer.getTime()
        trial_type = "Fixation"
        none = "None"
        super().write_tsv_csv(self.filename, self.filename_csv, [super().float_to_csv(onset), super().float_to_csv(time_long), trial_type, none, none, none])
        image_count=0
        for image_stim in liste_image_win:
            image_stim.draw()
            self.rect.draw()
            self.win.flip()
            if self.activation:
                super().send_character(self.port,self.baudrate)
            timer.reset()  # Réinitialiser le timer à chaque nouvelle image
            clicked = False  # Variable pour vérifier si un clic a été détecté
            clicked_time = "None"
            onset = self.global_timer.getTime()
            while timer.getTime() < duration:
                button = self.mouse.getPressed()  # Mise à jour de l'état des boutons de la souris

                if any(button):
                    if not clicked:  # Vérifier si c'est le premier clic détecté
                        clicked_time = timer.getTime()
                        print("Clic détecté à :", clicked_time, "secondes")
                        clicked = True  # Empêcher l'enregistrement de clics multiple
            time_long = timer.getTime()
            stimuli = images[image_count]
            trial_type = "Stimuli"
            if clicked_time != "None":
                clicked_time = super().float_to_csv(clicked_time)
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(time_long), trial_type, image_stim.ori, clicked_time, stimuli])
            cross_stim.draw()
            self.win.flip()
            onset = self.global_timer.getTime()
            timer.reset()
            while timer.getTime() < random.uniform(betweenstimuli-0.5, betweenstimuli+0.5):
                pass
            time_long = timer.getTime()
            stimuli = "None"
            trial_type = "Fixation"
            super().write_tsv_csv(self.filename, self.filename_csv,
                                  [super().float_to_csv(onset), super().float_to_csv(time_long), trial_type, "None", "None", stimuli])
            image_count+=1
        super().the_end(self.win)
        self.win.close()
        return stimulus_times, stimulus_apparition,stimuli_liste, orientation

    import os
    import csv
    from datetime import datetime

    def write_csv_and_tsv(self, onset, duration, file_stimuli, orientation, trial_type, filename="output"):
        output_dir = '../Fichiers_output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        current_date = datetime.now().strftime("%Y-%m-%d")
        run_number = 1
        filename_prefix = f"{current_date}_{filename}"

        existing_files = [f for f in os.listdir(output_dir) if f.startswith(filename_prefix) and 'run' in f]
        if existing_files:
            runs = [int(f.split('run')[-1].split('.')[0]) for f in existing_files if 'run' in f]
            if runs:
                run_number = max(runs) + 1

        csv_filename = os.path.join(output_dir, f"{filename_prefix}_run{run_number}.csv")
        tsv_filename = os.path.join(output_dir, f"{filename_prefix}_run{run_number}.tsv")

        # Écrire en CSV
        with open(csv_filename, mode='w', newline='') as file:
            csv_writer = csv.writer(file)  # Par défaut, utilise la virgule comme délimiteur
            csv_writer.writerow(['onset', 'duration', 'trial_type', 'angle', 'reaction', 'stim_file'])
            orientation.insert(3, 0)
            for x in range(len(trial_type)):
                if trial_type[x] == "Fixation":
                    orientation.insert(x, "None")
            for i in range(len(onset)):
                csv_writer.writerow(
                    [onset[i], duration[i], trial_type[i], orientation[i], self.click_times[i], file_stimuli[i]])

        # Écrire en TSV
        with open(tsv_filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')  # Utilise la tabulation comme délimiteur
            tsv_writer.writerow(['onset', 'duration', 'trial_type', 'angle', 'reaction', 'stim_file'])
            orientation.insert(3, 0)
            for x in range(len(trial_type)):
                if trial_type[x] == "Fixation":
                    orientation.insert(x, "None")
            for i in range(len(onset)):
                tsv_writer.writerow(
                    [onset[i], duration[i], trial_type[i], orientation[i], self.click_times[i], file_stimuli[i]])

    def lancement(self):
        stimulus_times, stimulus_apparition, stimuli, orientation = self.static_images_psychopy(self.file, self.duration, self.betweenstimuli)
        liste_trial=[]
        liste_lm=[]
        count=0
        for x in stimuli:
            if x == "Fixation":
                liste_lm.append(count)
                liste_trial.append("Fixation")
            else:
                liste_trial.append("Stimuli")
            count+=1
        for x in liste_lm:
            stimuli[x] = "None"



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=float, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--betweenstimuli", type=float, required=True, help="Durée en secondes entre les stimuli")
    parser.add_argument("--file", type=str, help="Chemin du fichier contenant les stimuli")
    parser.add_argument("--zoom", type=float, required=True, help="Pourcentage Zoom")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--activation", type=str, required=True, help="Pour le boitier avec les EEG")
    parser.add_argument("--random", type=str, required=True, help="Ordre random stimuli")
    parser.add_argument("--launching", type=str, help="Chemin vers le fichier de mots", required=False)



    parser.add_argument('--port', type=str, required=False, help="Port")
    parser.add_argument('--baudrate', type=int, required=False, help="Speed port")
    parser.add_argument('--trigger', type=str, required=False, help="caractère pour lancer le programme")
    parser.add_argument("--hauteur", type=float, required=True, help="hauteur du rectangle")
    parser.add_argument("--largeur", type=float, required=True, help="Largeur du rectangle")

    args = parser.parse_args()
    images = static_image(args.duration, args.betweenstimuli, args.file, args.zoom, args.output_file,
                          args.port, args.baudrate, args.trigger, args.activation, args.hauteur,
                          args.largeur, args.random, args.launching)
    images.lancement()