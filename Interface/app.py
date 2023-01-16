# Importation des modules nécessaires
import os
import re
import shutil

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from pylatexenc.latex2text import LatexNodes2Text

import pandas as pd

import azure.cognitiveservices.speech as speechsdk
import whisper

from pydub import AudioSegment

from saytex import Saytex 
import matplotlib
import matplotlib.pyplot as plt



# Chargement du modèle de reconnaissance de la parole
model = None
def load_model():
  global model
  model = whisper.load_model("base")



# Fonction de reconnaissance de la parole en texte
def Speech_To_Text(speech_audio): 
  """
  Transforme le fichier audio de la parole en texte
  """
  # Chargement du fichier audio et ajustement de sa durée à 30 secondes
  audio = whisper.load_audio(speech_audio)
  audio = whisper.pad_or_trim(audio)
  # Création du spectrogramme log-Mel et déplacement sur le même appareil que le modèle
  mel = whisper.log_mel_spectrogram(audio).to(model.device)
  # Détection de la langue parlée
  _, probs = model.detect_language(mel)
  detected_language = max(probs, key=probs.get)
  print("Langue détectée:", detected_language)

  # Décodage de l'audio
  options = whisper.DecodingOptions(fp16=False)
  result = whisper.decode(model, mel, options)

  return result.text, detected_language

# Fonction de conversion de texte en code LaTeX
def Text_To_Latex(text):
  """
  Transforme le texte en code LaTeX
  """
  # Utilisation de matplotlib sans interface graphique
  matplotlib.use('Agg')
  # Création d'un objet Saytex pour la conversion
  saytex_compiler = Saytex()
  try:
    # Application de la regex pour le nettoyage du texte
    text = Nettoyage(text)
    # Conversion du texte en code LaTeX
    latex_result = saytex_compiler.to_latex(text)
    # Enregistrement du résultat
    save_latex(latex_result)
    
  except:
    latex_result = "Erreur: Texte non reconnu en LaTeX"
  # Création de la figure matplotlib pour afficher le code LaTeX
  left, width, bottom, height = .30, .4, .25, .6; right = left + width; top = bottom + height
  fig = plt.figure()
  # Taille de la police en fonction de la longueur du texte
  fontsize = 75 if len(text.split(" ")) < 30 else 20
    # Affichage du code LaTeX sur la figure
  plt.text(0.5 *(left+right), 0.5*(bottom+top), "$"+ latex_result + "$", horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
  # Masquage des axes
  plt.axis('off')
  return latex_result, fig

# Fonction de conversion de code LaTeX en texte
def Latex_To_Text(latex):
  """
  Transforme le code LaTeX en texte
  """
  # Nettoyage du code LaTeX
  latex = latex.replace(f"\r", f'\\r')
  # Conversion du code LaTeX en texte
  text = LatexNodes2Text().latex_to_text(latex)
  return text

# Fonction de synthèse vocale
def Text_To_Speech(text, lang='fr', gender="female"):
  """
  Transforme le texte en parole synthétisée
  """
  # Clé d'abonnement et région de Azure Cognitive Services
  cle = "4c9e5aae707e41518A148720a8b56c11"
  region = "francecentral"
  # Configuration de la synthèse vocale
  speech_config = speechsdk.SpeechConfig(subscription=cle, region=region)
  audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
  # Sélection de la voix en fonction du genre et de la langue souhaités
  speech_config.speech_synthesis_voice_name = Speaker_Choice(gender=gender, language=lang)

  # Création de l'objet de synthèse vocale
  speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

  # Synthèse de la parole à partir du texte
  speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

  # Vérification du résultat de la synthèse vocale
  if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
      print("Speech synthesized for text [{}]".format(text))
  elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
      cancellation_details = speech_synthesis_result.cancellation_details
      print("Speech synthesis canceled: {}".format(cancellation_details.reason))
      if cancellation_details.reason == speechsdk.CancellationReason.Error:
          if cancellation_details.error_details:
              print("Error details: {}".format(cancellation_details.error_details))
              print("Did you set the speech resource key and region values?")


def simplify_multiplication(match_obj):
  if match_obj.group() is not None:
      to_change = match_obj.group()
      return to_change[:-1] + " times " + to_change[-1]

# Fonction de nettoyage du texte avec une regex
def Nettoyage(text):
  """
  Nettoyage du texte avec du regex et autre
  """
  # Clean the Text (get of last '.' and useless characters ',')
  text = text[:-1].replace(',', '') if text[-1] == "." else text.replace(',', '')
  # ax => a times x
  text = re.sub("\d+[a-z]+", simplify_multiplication, text) 
  # Simplify Power: x^4 = superscript 4 -> x power 4
  text = text.replace("power", "superscript").replace("^"," puissance ").replace("/"," sur ").replace("également", "equals")
  
  return text

def save_latex(latex):
  with open("static/latex.txt","w",encoding='utf-8') as f:
    f.write(latex)


# Fonction de sélection de la voix pour la synthèse vocale
def Speaker_Choice(gender="fr", language="female"):
  """
  Sélection de la voix en fonction du genre et de la langue souhaités
  """
  speaker_dict = {"fr": ["fr-FR-AlainNeural", "fr-FR-CelesteNeural"],
                  "en": ["en-GB-AlfieNeural", "en-US-AmberNeural"],
                  "es": ["es-ES-AlvaroNeural", "es-ES-AbrilNeural"],
                  "de": ["de-DE-BerndNeural", "de-DE-AmalaNeural"]}
  return speaker_dict[language][0] if gender == "male" else speaker_dict[language][1]




# Créer l'application Flask
app = Flask(__name__)

# Initialiser une variable de transcription vide
transcript = ""

# Définir la route principale et les méthodes HTTP autorisées
@app.route('/', methods=['GET','POST'])
def main():
  # Initialiser la variable de transcription vide à chaque requête
  transcript = ""
  # Ouvrir le fichier contenant le code LaTeX actuel
  with open("static/latex.txt","r") as f:
    latex = f.read()

  # Ouvrir le fichier contenant l'historique du code LaTeX
  with open("static/historique.txt","r") as f2:
    historique = f2.readlines()

  # Créer une liste des images de l'historique
  images = ["static/images/"+ i for i in os.listdir("static/images")[:-1]]
  # Si la méthode de la requête est POST
  if request.method == 'POST':
    # Si l'utilisateur a uploadé un fichier audio
    if "audio-file" in request.files:
      # Récupérer le fichier audio
      f = request.files["audio-file"]
      # Charger le fichier audio dans un objet AudioSegment
      segment = AudioSegment.from_file(f.stream)
      # Exporter l'audio au format WAV
      segment.export("static/audio/speech_file.wav", format="wav")

      try:
        # Transcrire l'audio en texte et générer le code LaTeX correspondant
        transcript,lang = Speech_To_Text("static/audio/speech_file.wav")
        transcript=Nettoyage(text=transcript)
        latex,fig = Text_To_Latex(transcript)
        # Enregistrer l'image de la formule générée
        image_path = "static/images/image_current.png"
        fig.savefig(image_path)
      except:
        # Afficher un message d'erreur en cas de problème de conversion audio
        print("Erreur de conversion Audio")

      # Afficher le texte transcrit
      print(transcript)
      # Rediriger vers la page principale
      return redirect(url_for("main"))
    else:
      # Ouvrir le fichier contenant le code LaTeX actuel
      with open("static/latex.txt","r",encoding='utf-8') as f:
        latex_text = f.read()
      # Générer et lire la version audio du code LaTeX
      Text_To_Speech(Nettoyage(Latex_To_Text(latex_text)))
      # Rediriger vers la page principale
      return redirect(url_for("main"))
  else:
    return render_template('main.html',transcript=transcript,historique=historique,latex=latex,images=images)



@app.route('/listening', methods=['GET','POST'])
def listen():
  # Générer le code LaTeX et l'image de la formule
  image_path = "static/images/image_current.png"
  # Afficher la page principale avec un message de image_current et l'image de la formule
  return render_template('main.html',message="image_current",image_path=image_path)



# Définir la route de la page de sauvegarde de l'historique et les méthodes HTTP autorisées
@app.route('/save_current_to_historic', methods=['GET','POST'])
def save_to_historic():
  # Si la méthode de la requête est POST
  if request.method == 'POST':
  # Récupérer la valeur actuelle (code LaTeX)
    current = request.form["current_value"]
  # Récupérer la liste des images de l'historique
  images = os.listdir("static/images")
  # Définir le nom de l'image à enregistrer
  image_historique = "image_"+ str(len(images)-1) +".png"
  # Copier l'image actuelle vers l'historique
  shutil.copy("static/images/image_current.png", "static/images/"+image_historique)
  # Ouvrir le fichier contenant l'historique du code LaTeX
  with open("static/historique.txt","r") as f:
    historic = f.read()
  # Ajouter la valeur actuelle (code LaTeX) à l'historique
  with open("static/historique.txt","w") as f:
    f.write(historic+"\n"+Latex_To_Text(current))

  # Rediriger vers la page principale
  return redirect(url_for("main"))



# Définir la route de la page de suppression de l'historique et les méthodes HTTP autorisées
@app.route('/clear_historic', methods=['GET','POST'])
def clear_historic():
  # Si la méthode de la requête est POST
  if request.method == 'POST':
  # Vider le fichier contenant l'historique du code LaTeX
    with open("static/historique.txt","w",encoding='utf-8') as f:
      f.write("")
    for file in os.listdir("static/images/"):
      if file.startswith("image_"):
        # Supprimer toutes les images de l'historique
        os.remove("static/images/"+file)
  # Rediriger vers la page principale
  return redirect(url_for("main"))


if __name__ == '__main__':
  # Charger le modèle
  load_model()
  # Lancer l'application Flask en mode débogage
  app.run(debug = True)