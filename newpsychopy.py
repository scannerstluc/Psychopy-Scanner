import random

from psychopy import visual, core, event

win = visual.Window(fullscr=True, color=[-1, -1, -1])

Premier_texte = ("Dans l'exercice qui va suivre vous verrez apparaitre des adjectifs. \n"+
                 "Suivant la consigne, vous devrez juger pour chaque adjectif: \n"+
                 "-comment il s'applique à vous-même \n"+
                 "-comment il s'applique à votre meilleur(e) ami(e) \n"+
                 "-ou alors donner le nombre de syllabes qui le composent\n\n"+
                 "(appuyer sur une touche pour lire la suite)")

texte = visual.TextStim(win, text=Premier_texte, color=[1, 1, 1], alignText="left", wrapWidth=1.5 )
texte.draw()
win.flip()
event.waitKeys()

Deuxieme_texte= ('Dans la consigne "MOI" vous devez dire dans quelle mesure l\'adjectif s\'applique à vous.\n \n'+
                 'Dans la consigne "MON AMI(E)" vous devez indiquer comment l\'adjectif s\'applique à votre meilleur(e) ami(e).\n\n'+
                 'Vous répondrez avec les touches suivantes:\n'+
                 '1 (index) : ne s\'applique pas du tout \n'+
                 '2 (majeur) : s\'applique un peu\n'+
                 '3 (annulaire) : s\'applique assez bien\n'+
                 '4 (auriculaire) : s\'applique parfaitement\n\n'+
                 '(appuyer sur une touche pour lire la suite)')

texte.text=Deuxieme_texte
texte.draw()
win.flip()
event.waitKeys()

troisieme_texte = ('Dans la consigne "SYLLABES" vous devez donner le nombre de syllabes qui composent l\'adjectif en appuyant sur la touche correspondate: '+
                   '1, 2, 3 ou 4 syllabe(s) \n\n'+
                   'Par exemple: \n'+
                   'le mot "attentif" a 3 syllabes: at-ten-tif\n\n'+
                   'Les mots défileront automatiquement, essayez de répondre pour chacun d\'eux le plus spontanément possible\n\n'+
                   '(appuyer sur une touche pour lire la suite)')

texte.text=troisieme_texte
texte.draw()
win.flip()
event.waitKeys()

quatrieme_texte = ('A présent nous allons faire un court entrainement pour vous familiariser avec l\'exercise.\n\n'+
                   '(appuyer sur une touche pour lire la suite)')

texte.text= quatrieme_texte
texte.draw()
win.flip()
event.waitKeys()

cinquieme_texte = ('Veuillez penser à la personne que vous considérez votre meilleur(e) ami(e).\n'+
                   'Il est important que vous soyez capable de la décrire mentalement '+
                   'de façon assez précise \n\n'+
                   'Prenez votre temps...\n\n'+
                   'Quand vous êtes prèt(e), appuyez sur une touche pour démarrer l\'entrainement...')

texte.text= cinquieme_texte
texte.draw()
win.flip()
event.waitKeys()

Me_shortcue = ('MOI \n\n'+
               'Comment l\'adjectif s\'applique à moi?')

Friend_shortcue = ('MON AMI(E) [this could be someone else of course]\n\n'
    +'Comment l\'adjectif s\'applique-t-il à mon/ma meilleur(e) ami(e) ?')

Syllabe_shortcue = ('SYLLABES\n\n' +
                    'Combien de syllables de comporte cet adjectif?')




def debut_me():
    texte_block = visual.TextStim(win, text=Me_shortcue, color=[1, 1, 1], alignText="left", wrapWidth=1.5)
    clock = core.Clock()
    texte_block.draw()
    win.flip()
    while clock.getTime() < 3:
        pass

def debut_friend():
    texte_block = visual.TextStim(win, text=Friend_shortcue, color=[1, 1, 1], alignText="left", wrapWidth=1.5)
    clock = core.Clock()
    texte_block.draw()
    win.flip()
    while clock.getTime() < 3:
        pass

def debut_syllabe():
    texte_block = visual.TextStim(win, text=Syllabe_shortcue, color=[1, 1, 1], alignText="left", wrapWidth=1.5)
    clock = core.Clock()
    texte_block.draw()
    win.flip()
    while clock.getTime() < 3:
        pass

class list_words:
    def __init__(self):
        self.words=  [
            "sincère", "gentil", "fiable", "chaleureux", "poli", "ponctuel",
            "intelligent", "imaginatif", "confiant", "énergisé", "généreux",
            "loyal", "gai", "doué", "sociable", "indépendant", "efficace",
            "romantique", "patient", "tolérant", "curieux", "soigneux",
            "comique", "créative", "responsable","jaloux", "ragoteur",
            "cruel", "grande-gueule", "colérique", "querelleur", "possessif",
            "dépensier", "paresseux", "pessimiste", "brouillon", "maladroit",
            "égoïste", "malhonnête", "irritable", "ennuyant", "mufle",
            "indifférent", "désordonné", "hypersensible", "dominateur",
            "obtus", "indiscret", "vantard", "irresponsable"
        ]

        self.me_blocks = self.words.copy()
        self.friend_blocks = self.words.copy()
        self.syllabe_blocks = self.words.copy()

    def show_1_word(self, mot):
        texte_4_words = visual.TextStim(win, color=[1, 1, 1], alignText="left", wrapWidth=1.5)
        texte_4_words.text = mot
        texte_4_words.draw()
        win.flip()
        clock = core.Clock()
        while clock.getTime() < 4:  # Limite de temps de 4 secondes
            keys = event.getKeys()  # Récupérer les touches pressées
            if "1" in keys or "2" in keys or '3' in keys or "4" in keys :
                break  # Sortir de la boucle si une des touches est pressée

        win.flip()

    def show_4_words(self, block_type):
        mot1="";mot2="";mot3="";mot4=""
        if block_type == "me":
            mot1=random.choice(self.me_blocks)
            self.me_blocks.remove(mot1)
            mot2=random.choice(self.me_blocks)
            self.me_blocks.remove(mot2)
            mot3=random.choice(self.me_blocks)
            self.me_blocks.remove(mot3)
            mot4=random.choice(self.me_blocks)
            self.me_blocks.remove(mot4)

        if block_type == "friend":
            mot1=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot1)
            mot2=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot2)
            mot3=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot3)
            mot4=random.choice(self.friend_blocks)
            self.friend_blocks.remove(mot4)

        if block_type == "syllabe":
            mot1=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot1)
            mot2=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot2)
            mot3=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot3)
            mot4=random.choice(self.syllabe_blocks)
            self.syllabe_blocks.remove(mot4)

        self.show_1_word(mot1)
        self.show_1_word(mot2)
        self.show_1_word(mot3)
        self.show_1_word(mot4)


debut_me()
showner = list_words()
showner.show_4_words("me")



win.close()
core.quit()
