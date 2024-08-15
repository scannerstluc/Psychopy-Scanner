import speech_recognition as sr

# Créer un objet Recognizer

def reconnaissance():
    recognizer = sr.Recognizer()

    audio_file = "Fichiers_output/2024-08-14_ififi_run3/2024-08-14_ififi_run3_record1.wav"

    # Utiliser SpeechRecognition pour convertir l'audio en texte
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="fr-FR")
            return text
        except sr.UnknownValueError:
            return "None/pas reconnu"
            print("Google Speech Recognition n'a pas pu comprendre l'audio")
        except sr.RequestError as e:
            return "None/pas reconnu"
            print(f"Erreur lors de la demande à Google Speech Recognition; {e}")

print(2%2)
