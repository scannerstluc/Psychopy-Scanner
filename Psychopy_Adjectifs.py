import csv
import os
import random
from datetime import datetime

import argparse
from psychopy import visual, core, event
import threading





class Adjectifs:

    def __init__(self, duration, betweenstimuli, zoom, blocks, filepath, output):
        self.words=  self.reading("Paradigme_Adjectifs/"+filepath)
        self.me_blocks = self.words.copy()
        self.friend_blocks = self.words.copy()
        self.syllabe_blocks = self.words.copy()
        self.Syllabe_shortcue=""
        self.Me_shortcue=""
        self.Friend_shortcue=""
        self.shown_words = []
        self.order_blocks = []
        self.reaction_time = []
        self.response = []

        self.stimuli_duration = duration
        self.betweenstimuli = betweenstimuli
        self.zoom = zoom
        self.filepath = filepath
        self.output = output
        self.number_of_blocks = blocks

        self.win = visual.Window(fullscr=True)

        event.globalKeys.add(key='escape', func=self.win.close)

    def check_for_esc(self):
        if 'escape' in event.getKeys():
            self.win.close()
            core.quit()

    def reading(self,filename):
        with open(filename, "r", encoding="utf-8") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

    def lancement(self):


        self.Premier_texte = ("Dans l'exercice qui va suivre vous verrez apparaitre des adjectifs. \n" +
                         "Suivant la consigne, vous devrez juger pour chaque adjectif: \n\n" +
                         "-comment il s'applique à vous-même \n" +
                         "-comment il s'applique à votre meilleur(e) ami(e) \n" +
                         "-ou alors donner le nombre de syllabes qui le composent\n\n" +
                         "(appuyer sur une touche pour lire la suite)")

        texte = visual.TextStim(self.win, text=self.Premier_texte, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font='Arial')
        texte.draw()
        self.win.flip()
        event.waitKeys()

        Deuxieme_texte = (
                    'Dans la consigne "MOI" vous devez dire dans quelle mesure l\'adjectif s\'applique à vous.\n \n' +
                    'Dans la consigne "MON AMI(E)" vous devez indiquer comment l\'adjectif s\'applique à votre meilleur(e) ami(e).\n\n' +
                    'Vous répondrez avec les touches suivantes:\n' +
                    '1 (index) : ne s\'applique pas du tout \n' +
                    '2 (majeur) : s\'applique un peu\n' +
                    '3 (annulaire) : s\'applique assez bien\n' +
                    '4 (auriculaire) : s\'applique parfaitement\n\n' +
                    '(appuyer sur une touche pour lire la suite)')

        texte.text = Deuxieme_texte
        texte.draw()
        self.win.flip()
        event.waitKeys()

        troisieme_texte = (
                    'Dans la consigne "SYLLABES" vous devez donner le nombre de syllabes qui composent l\'adjectif en appuyant sur la touche correspondate: ' +
                    '1, 2, 3 ou 4 syllabe(s) \n\n' +
                    'Par exemple: \n' +
                    'le mot "attentif" a 3 syllabes: at-ten-tif\n\n' +
                    'Les mots défileront automatiquement, essayez de répondre pour chacun d\'eux le plus spontanément possible\n\n' +
                    '(appuyer sur une touche pour lire la suite)')

        texte.text = troisieme_texte
        texte.draw()
        self.win.flip()
        event.waitKeys()

        quatrieme_texte = (
                    'A présent nous allons faire un court entrainement pour vous familiariser avec l\'exercise.\n\n' +
                    '(appuyer sur une touche pour lire la suite)')

        texte.text = quatrieme_texte
        texte.draw()
        self.win.flip()
        event.waitKeys()

        cinquieme_texte = ('Veuillez penser à la personne que vous considérez votre meilleur(e) ami(e).\n' +
                           'Il est important que vous soyez capable de la décrire mentalement ' +
                           'de façon assez précise \n\n' +
                           'Prenez votre temps...\n\n' +
                           'Quand vous êtes prèt(e), appuyez sur une touche pour démarrer l\'entrainement...')

        texte.text = cinquieme_texte
        texte.draw()
        self.win.flip()
        event.waitKeys()

        self.Me_shortcue = ('MOI \n\n' +
                       'Comment l\'adjectif s\'applique à moi?')

        self.Friend_shortcue = ('MON AMI(E) [this could be someone else of course]\n\n'
                           + 'Comment l\'adjectif s\'applique-t-il à mon/ma meilleur(e) ami(e) ?')

        self.Syllabe_shortcue = ('SYLLABES\n\n' +
                            'Combien de syllables comporte cet adjectif?')

    def debut_me(self):
        texte_block = visual.TextStim(self.win, text=self.Me_shortcue, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass

    def debut_friend(self):
        texte_block = visual.TextStim(self.win, text=self.Friend_shortcue, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass

    def debut_syllabe(self):
        texte_block = visual.TextStim(self.win, text=self.Syllabe_shortcue, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass



    def show_1_word(self, mot):
        texte_5_words = visual.TextStim(self.win, color=[1, 1, 1], wrapWidth=1.5, font="Arial", height=0.1+(0.001*self.zoom))
        texte_5_words.text = mot
        texte_5_words.draw()
        self.win.flip()
        response_time="None"
        timer = core.Clock()
        k="None"
        while timer.getTime() < self.stimuli_duration:  # Limite de temps de 4 secondes
            if k=="None":
                key = event.getKeys()  # Récupérer les touches pressées
                if "1" in key or "2" in key or '3' in key or "4" in key :
                    k=key
                    response_time=timer.getTime()
                    texte_5_words.text=" "
                    texte_5_words.draw()
                    self.win.flip()
        self.response.append(k)
        self.reaction_time.append(response_time)


        self.win.flip()

    def show_5_words(self, block_type):
        mot1="";mot2="";mot3="";mot4="";mot5=""
        if block_type == "me":
            mot1=random.choice(self.me_blocks)
            self.me_blocks.remove(mot1)
            mot2=random.choice(self.me_blocks)
            self.me_blocks.remove(mot2)
            mot3=random.choice(self.me_blocks)
            self.me_blocks.remove(mot3)
            mot4=random.choice(self.me_blocks)
            self.me_blocks.remove(mot4)
            mot5 = random.choice(self.me_blocks)
            self.me_blocks.remove(mot5)

        if block_type == "friend":
            mot1=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot1)
            mot2=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot2)
            mot3=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot3)
            mot4=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot4)
            mot5 = random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot5)

        if block_type == "syllabe":
            mot1=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot1)
            mot2=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot2)
            mot3=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot3)
            mot4=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot4)
            mot5 = random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot5)

        self.show_1_word(mot1)
        self.show_1_word(mot2)
        self.show_1_word(mot3)
        self.show_1_word(mot4)
        self.show_1_word(mot5)
        self.shown_words.append(mot1)
        self.shown_words.append(mot2)
        self.shown_words.append(mot3)
        self.shown_words.append(mot4)
        self.shown_words.append(mot5)

    def write_tsv(self, filename="output1.tsv"):
        filename = self.output
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
            tsv_writer.writerow(['block_type', 'word', 'response', 'response_time'])
            pred = 0
            count = 0
            for i in range(len(self.shown_words)):
                if count == 5:
                    pred += 1
                    count = 0
                print(pred)
                tsv_writer.writerow(
                    [self.order_blocks[pred], self.shown_words[i], self.response[i], self.reaction_time[i]])
                count += 1

    def blocks(self):
        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )

        number_of_blocks = self.number_of_blocks
        choice_block = ["me", "friend", "syllabe"]
        hashmap = {"me": 10, "friend": 10, "syllabe": 10}
        clock = core.Clock()

        for x in range(number_of_blocks):
            if len(choice_block)==0:
                break
            block = random.choice(choice_block)
            self.order_blocks.append(block)
            hashmap[block] -= 1
            if hashmap[block] == 0:
                choice_block.remove(block)

            if block == "me":
                self.debut_me()
                self.show_5_words(block)
            elif block == "friend":
                self.debut_friend()
                self.show_5_words(block)
            elif block == "syllabe":
                self.debut_syllabe()
                self.show_5_words(block)

            # Affichage de la croix de fixation pendant 100 secondes
            cross_stim.draw()
            self.win.flip()
            fixation_duration = self.betweenstimuli  # en secondes
            clock.reset()

            while clock.getTime() < fixation_duration:
                cross_stim.draw()
                self.win.flip()

    def fin(self):
        print(self.shown_words)
        print(self.order_blocks)
        print(self.reaction_time)
        print(self.response)
        self.win.close()
        self.write_tsv()
        core.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécuter le paradigme Psychopy")
    parser.add_argument("--duration", type=int, required=True, help="Durée en secondes des stimuli")
    parser.add_argument("--file", type=str, help="Chemin vers le fichier de mots", required=False)
    parser.add_argument("--zoom", type=int, required=True, help="Le zoom sur les adjectifs")
    parser.add_argument("--output_file", type=str, required=True, help="Nom du fichier d'output")
    parser.add_argument("--betweenstimuli", type=int, required=True, help="Temps entre les stimuli")
    parser.add_argument("--blocks", type=int, required=True, help="Nombre de blocks d'adjectifs")


    args = parser.parse_args()
    paradigm = Adjectifs(args.duration, args.betweenstimuli, args.zoom, args.blocks, args.file, args.output_file)
    paradigm.lancement()
    paradigm.blocks()
    paradigm.fin()


