import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from psychopy import visual, core, event

# Configuration de la fenêtre
win = visual.Window([800, 600])

# Configuration du stimulus de texte
text_stim = visual.TextStim(win, text="Dites quelque chose!")

# Afficher le stimulus de texte
text_stim.draw()
win.flip()

# Configurer les paramètres de l'enregistrement
fs = 44100  # Fréquence d'échantillonnage
duration = 5  # Durée de l'enregistrement en secondes

# Démarrer l'enregistrement audio
print("Enregistrement en cours...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()  # Attendre la fin de l'enregistrement
print("Enregistrement terminé.")

# Sauvegarder l'enregistrement
write("enregistrement.wav", fs, recording)

win.close()
core.quit()