from psychopy import sound, core

# Charger le fichier audio
audio = sound.Sound('../Input/Paradigme_EMO_VOICES/emo_voices/norm_01col126.wav')  # Remplacez par le chemin de votre fichier audio

# Jouer le fichier audio
audio.play()

# Attendre la fin de la lecture
core.wait(audio.getDuration())

# Fin du script
core.quit()
