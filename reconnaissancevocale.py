import streamlit as st
import speech_recognition as sr


# Créer une fonction pour la reconnaissance vocale
def transcribe_speech(api_name, language, filename=None):
    recognizer = sr.Recognizer()

    if api_name == "google":
        recognizer.recognize_function = recognizer.recognize_google
    elif api_name == "sphinx":
        recognizer.recognize_function = recognizer.recognize_sphinx
    else:
        st.error("API non prise en charge.")
        return

    st.write(f"Parlez quelque chose en {language}...")
    audio_text = ""

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            audio_text = recognizer.recognize_function(audio, language=language)
        except sr.UnknownValueError:
            st.warning("Désolé, je n'ai pas pu comprendre ce que vous avez dit.")
        except sr.RequestError as e:
            st.error(f"Une erreur est survenue lors de la requête à l'API : {e}")

    if audio_text:
        st.success("Texte reconnu :")
        st.write(audio_text)

        if filename:
            with open(filename, "a") as file:
                file.write(audio_text + "\n")


# Créer une application Streamlit
st.title("Reconnaissance Vocale avec Streamlit")

option = st.selectbox("Sélectionnez une option :", ["Reconnaissance vocale (Google)", "Reconnaissance vocale (Sphinx)"])
language = st.selectbox("Sélectionnez la langue :", ["en-US", "fr-FR"])
filename = st.text_input("Nom du fichier de sauvegarde (laissez vide pour ne pas enregistrer) :")

if st.button("Commencer la reconnaissance vocale"):
    if "Google" in option:
        transcribe_speech("google", language, filename)
    else:
        transcribe_speech("sphinx", language, filename)
