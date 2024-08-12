import speech_recognition as sr

# Créer un objet Recognizer
recognizer = sr.Recognizer()

# Charger le fichier audio converti
audio_file = "enregistrement_pcm.wav"

# Utiliser SpeechRecognition pour convertir l'audio en texte
with sr.AudioFile(audio_file) as source:
    audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language="fr-FR")
        print("Texte reconnu :")
        print(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition n'a pas pu comprendre l'audio")
    except sr.RequestError as e:
        print(f"Erreur lors de la demande à Google Speech Recognition; {e}")
