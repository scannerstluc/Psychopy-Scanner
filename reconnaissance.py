import sounddevice as sd
import soundfile as sf
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

# Démarrer l'enregistrement audio en PCM 16-bit
print("Enregistrement en cours...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
sd.wait()  # Attendre la fin de l'enregistrement
print("Enregistrement terminé.")

# Sauvegarder l'enregistrement directement en format WAV PCM 16-bit
sf.write("enregistrement_pcm.wav", recording, fs)

# Fermer la fenêtre PsychoPy
win.close()
core.quit()
