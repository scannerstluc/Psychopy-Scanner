import sounddevice as sd
import soundfile as sf
import numpy as np
from psychopy import visual, core, event
win = visual.Window(fullscr=True, color="black")
event.globalKeys.add(key='escape', func=win.close)
fs = 44100  # fréquence d'échantillonnage
duration = 2  # durée de l'enregistrement en secondes
threshold = 1000  # seuil pour détecter le début de la parole (à ajuster selon votre micro/environnement)
clock = core.Clock()  # création de l'horloge
patient_id = "Patient1_"

liste_mots= ["bonjour", "fonctionne"]
cross_stim = visual.ShapeStim(
        win=win,
        vertices=((0, -0.03), (0, 0.03), (0, 0), (-0.03, 0), (0.03, 0)),  # Utilisation d'unités normalisées
        lineWidth=3,
        closeShape=False,
        lineColor="white",
        units='height'  # Utilisation d'unités basées sur la hauteur de l'écran
    )

def reading(filename):
    words = []
    colors = []
    with open(filename, "r", encoding="utf-8") as fichier:
        for line in fichier:
            parts = line.strip().split(',')
            if len(parts) == 2:
                words.append(parts[0].strip())
                colors.append(parts[1].strip())
    return words, colors


words, colors=reading("Paradigme_Couleur/colors_list.txt")
images = []
text_stim = visual.TextStim(win)
count=0
for mot in words:
    cross_stim.draw()
    win.flip()
    clock.reset()
    while clock.getTime() < 2:
        pass
    text_stim.text=mot
    text_stim.color=colors[count]
    text_stim.draw()
    win.flip()
    print("Enregistrement en cours...")
    clock.reset()
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Enregistrement terminé.")
    start_time = None
    for i, sample in enumerate(recording):
        if np.abs(sample) > threshold:
            start_time = i / fs
            break
    if start_time is not None:
        print(f"L'utilisateur a commencé à parler à {start_time:.2f} secondes.")
    else:
        print("Aucune parole détectée.")

    mot = "run" + str(count)
    count+=1

    # Sauvegarde de l'enregistrement
    sf.write(patient_id+mot+".wav", recording, fs)


win.close()
core.quit()
