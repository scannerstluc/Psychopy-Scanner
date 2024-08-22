import csv
import os
import random
from datetime import datetime

import argparse
from psychopy import visual, core, event
from Paradigme_parent import Parente
import serial






class Adjectifs(Parente):

    def __init__(self, duration, betweenstimuli, zoom, blocks, entrainement, per_block, filepath, output, port, baudrate, trigger):
        self.words = self.reading("Input/Paradigme_Adjectifs/"+filepath)
        self.entrainement_words = self.reading("Input/Paradigme_Adjectifs/entrainement.txt")
        self.me_entrainement = self.entrainement_words.copy()
        self.friend_entrainement = self.entrainement_words.copy()
        self.syllable_entrainement = self.entrainement_words.copy()
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
        self.entrainement_block = entrainement
        self.per_block = per_block
        self.experience_text = ""
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(self.port, self.baudrate)

        self.win = visual.Window(fullscr=True)
        self.explication_texts = super().inputs_texts("Input/Starting_Texts/adjectifs.txt")

        event.globalKeys.add(key='escape', func=self.win.close)

    def waiting_boitier(self):
        while True:
            if self.ser.in_waiting > 0:
                self.ser.read().decode('utf-8')
                break



    def reading(self,filename):
        with open(filename, "r", encoding="utf-8") as fichier:
            ma_liste = [line.strip() for line in fichier]
        return ma_liste

    def lancement(self):


        self.Premier_texte = self.explication_texts[0]

        """("Dans l'exercice qui va suivre vous verrez apparaitre des adjectifs. \n" +
                     "Suivant la consigne, vous devrez juger pour chaque adjectif: \n\n" +
                     "-comment il s'applique à vous-même \n" +
                     "-comment il s'applique à votre meilleur(e) ami(e) \n" +
                     "-ou alors donner le nombre de syllabes qui le composent\n\n" +
                     "(appuyer sur une touche pour lire la suite)")"""

        texte = visual.TextStim(self.win, text=self.Premier_texte, color=[1, 1, 1], alignText="left", wrapWidth=1.5, font='Arial')
        texte.draw()
        self.win.flip()
        self.waiting_boitier()
        #event.waitKeys()
        Deuxieme_texte = self.explication_texts[1]
        """
        Deuxieme_texte = (
                    'Dans la consigne "MOI" vous devez dire dans quelle mesure l\'adjectif s\'applique à vous.\n \n' +
                    'Dans la consigne "MON AMI(E)" vous devez indiquer comment l\'adjectif s\'applique à votre meilleur(e) ami(e).\n\n' +
                    'Vous répondrez avec les touches suivantes:\n' +
                    '1 (index) : ne s\'applique pas du tout \n' +
                    '2 (majeur) : s\'applique un peu\n' +
                    '3 (annulaire) : s\'applique assez bien\n' +
                    '4 (auriculaire) : s\'applique parfaitement\n\n' +
                    '(appuyer sur une touche pour lire la suite)')"""

        texte.text = Deuxieme_texte
        texte.draw()
        self.win.flip()
        self.waiting_boitier()
        #event.waitKeys()
        troisieme_texte = self.explication_texts[2]
        """troisieme_texte = (
                    'Dans la consigne "SYLLABES" vous devez donner le nombre de syllabes qui composent l\'adjectif en appuyant sur la touche correspondate: ' +
                    '1, 2, 3 ou 4 syllabe(s) \n\n' +
                    'Par exemple: \n' +
                    'le mot "attentif" a 3 syllabes: at-ten-tif\n\n' +
                    'Les mots défileront automatiquement, essayez de répondre pour chacun d\'eux le plus spontanément possible\n\n' +
                    '(appuyer sur une touche pour lire la suite)')"""

        texte.text = troisieme_texte
        texte.draw()
        self.win.flip()
        self.waiting_boitier()
        #event.waitKeys()

        quatrieme_texte = self.explication_texts[3]
        """quatrieme_texte = (
                    'A présent nous allons faire un court entrainement pour vous familiariser avec l\'exercise.\n\n' +
                    '(appuyer sur une touche pour lire la suite)')"""

        texte.text = quatrieme_texte
        texte.draw()
        self.win.flip()
        self.waiting_boitier()
        #event.waitKeys()

        cinquieme_texte = self.explication_texts[4]
        """cinquieme_texte = ('Veuillez penser à la personne que vous considérez votre meilleur(e) ami(e).\n' +
                           'Il est important que vous soyez capable de la décrire mentalement ' +
                           'de façon assez précise \n\n' +
                           'Prenez votre temps...\n\n' +
                           'Quand vous êtes prèt(e), appuyez sur une touche pour démarrer l\'entrainement...')"""

        texte.text = cinquieme_texte
        texte.draw()
        self.win.flip()
        self.waiting_boitier()
        #event.waitKeys()

        self.experience_text = self.explication_texts[5]


        self.Me_shortcue = self.explication_texts[6]
        """self.Me_shortcue = ('MOI \n\n' +
                       'Comment l\'adjectif s\'applique à moi?')"""


        self.Friend_shortcue = self.explication_texts[7]
        """self.Friend_shortcue = ('MON AMI(E) [this could be someone else of course]\n\n'
                           + 'Comment l\'adjectif s\'applique-t-il à mon/ma meilleur(e) ami(e) ?')"""

        self.Syllabe_shortcue = self.explication_texts[8]
        """self.Syllabe_shortcue = ('SYLLABES\n\n' +
                            'Combien de syllables comporte cet adjectif?')"""

        self.entrainement()
        texte.text = self.experience_text
        texte.draw()
        self.win.flip()
        self.waiting_boitier()
        self.blocks()


    def debut_me(self):
        texte_block = visual.TextStim(self.win, text=self.Me_shortcue, color=[1, 1, 1], alignText="center", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass

    def debut_friend(self):
        texte_block = visual.TextStim(self.win, text=self.Friend_shortcue, color=[1, 1, 1], alignText="center", wrapWidth=1.5, font="Arial")
        clock = core.Clock()
        texte_block.draw()
        self.win.flip()
        while clock.getTime() < 3:
            pass

    def debut_syllabe(self):
        texte_block = visual.TextStim(self.win, text=self.Syllabe_shortcue, color=[1, 1, 1], alignText="center", wrapWidth=1.5, font="Arial")
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
                if self.ser.in_waiting>0:
                    key = self.ser.read().decode('utf-8') # Récupérer les touches pressées
                    #ser.read().decode('utf-8')
                    if "1" in key or "2" in key or '3' in key or "4" in key :
                        k=key
                        response_time=timer.getTime()
                        texte_5_words.text=" "
                        texte_5_words.draw()
                        self.win.flip()
        self.response.append(k)
        self.reaction_time.append(response_time)


        self.win.flip()


    def show_words(self,count, block_type):
        if count !=0:
            print(count)

            mot=""
            if block_type == "me":
                mot = random.choice(self.me_blocks)
                self.me_blocks.remove(mot)
            if block_type == "friend":
                mot=random.choice(self.friend_blocks)
                self.friend_blocks.remove(mot)
            if block_type == "syllabe":
                mot=random.choice(self.syllabe_blocks)
                self.syllabe_blocks.remove(mot)
            self.show_1_word(mot)
            print(mot)
            print(block_type)
            self.shown_words.append(mot)
            self.order_blocks.append(block_type)
            self.show_words(count-1,block_type)


    def write_tsv(self,):
        filename= self.output
        filename = super().preprocessing_tsv(filename)

        with open(filename, mode='w', newline='') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['block_type', 'word', 'response', 'response_time'])
            pred = 0
            count = 0
            for i in range(len(self.shown_words)):
                tsv_writer.writerow(
                    [self.order_blocks[i], self.shown_words[i], self.response[i], self.reaction_time[i]])
                count += 1

    def entrainement_show_words(self, count, block_type):
        if count !=0:
            print(count)

            mot=""
            if block_type == "me":
                mot = random.choice(self.me_entrainement)
                self.me_entrainement.remove(mot)
            if block_type == "friend":
                mot=random.choice(self.friend_entrainement)
                self.friend_entrainement.remove(mot)
            if block_type == "syllabe":
                mot=random.choice(self.syllable_entrainement)
                self.syllable_entrainement.remove(mot)
            self.show_1_word(mot)
            print(mot)
            print(block_type)
            self.entrainement_show_words(count-1,block_type)

    def entrainement(self):
        cross_stim = visual.ShapeStim(
            win=self.win,
            vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
            lineWidth=3,
            closeShape=False,
            lineColor="white",
            units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
        )

        number_of_blocks = self.entrainement_block
        choice_block = ["me", "friend", "syllabe"]
        longueur = len(self.entrainement_words) // self.per_block
        hashmap = {"me": longueur, "friend": longueur, "syllabe": longueur}
        clock = core.Clock()

        for x in range(number_of_blocks):
            if len(choice_block) == 0:
                break
            block = random.choice(choice_block)
            print(block)
            hashmap[block] -= 1
            if hashmap[block] == 0:
                choice_block.remove(block)

            if block == "me":
                print("dans me")
                self.debut_me()
                self.entrainement_show_words(self.per_block, block)
                # self.show_5_words(block)
            elif block == "friend":
                print("dans friend")
                self.debut_friend()
                self.entrainement_show_words(self.per_block, block)
                # self.show_5_words(block)
            elif block == "syllabe":
                print("dans syllabe")
                self.debut_syllabe()
                self.entrainement_show_words(self.per_block, block)
                # self.show_5_words(block)

            # Affichage de la croix de fixation pendant 100 secondes
            cross_stim.draw()
            self.win.flip()
            fixation_duration = self.betweenstimuli  # en secondes
            clock.reset()

            while clock.getTime() < fixation_duration:
                cross_stim.draw()
                self.win.flip()

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
        longueur = len(self.words)//self.per_block
        hashmap = {"me": longueur, "friend": longueur, "syllabe": longueur}
        clock = core.Clock()

        for x in range(number_of_blocks):
            if len(choice_block)==0:
                break
            block = random.choice(choice_block)
            #self.order_blocks.append(block)
            print(block)
            hashmap[block] -= 1
            if hashmap[block] == 0:
                choice_block.remove(block)

            if block == "me":
                print("dans me")
                self.debut_me()
                self.show_words(self.per_block,block)
                #self.show_5_words(block)
            elif block == "friend":
                print("dans friend")
                self.debut_friend()
                self.show_words(self.per_block,block)
                #self.show_5_words(block)
            elif block == "syllabe":
                print("dans syllabe")
                self.debut_syllabe()
                self.show_words(self.per_block,block)
                #self.show_5_words(block)

            # Affichage de la croix de fixation pendant 100 secondes
            cross_stim.draw()
            self.win.flip()
            fixation_duration = self.betweenstimuli  # en secondes
            clock.reset()

            while clock.getTime() < fixation_duration:
                cross_stim.draw()
                self.win.flip()

    def fin(self):
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
    parser.add_argument("--entrainement", type=int, required=True, help="Nombre de blocks d'entrainement")
    parser.add_argument('--port', type=str, required=True, help="Port")
    parser.add_argument('--baudrate', type=int, required=True, help="Speed port")
    parser.add_argument('--trigger', type=str, required=True, help="caractère pour lancer le programme")
    parser.add_argument("--per_block", type=int, required=True, help="Nombre d'adjectifs pas block")



    args = parser.parse_args()
    paradigm = Adjectifs(args.duration, args.betweenstimuli, args.zoom, args.blocks, args.entrainement, args.per_block, args.file, args.output_file, args.port, args.baudrate, args.trigger)
    paradigm.lancement()
    paradigm.fin()


