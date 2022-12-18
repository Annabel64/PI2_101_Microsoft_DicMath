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

model = None
def load_model():
  global model
  model = whisper.load_model("base")

def text_to_readable(text):
  return text.replace("^"," puissance ").replace("/"," sur ").replace("-"," moins ")
def Speaker_Choice(language="fr", gender="male"):
    speaker_dict = {"fr": ["fr-FR-AlainNeural", "fr-FR-CelesteNeural"],
                    "en": ["en-GB-AlfieNeural", "en-US-AmberNeural"],
                    "es": ["es-ES-AlvaroNeural", "es-ES-AbrilNeural"],
                    "de": ["de-DE-BerndNeural", "de-DE-AmalaNeural"]}
    return speaker_dict[language][0] if gender == "male" else speaker_dict[language][1]

def text2speech(text, lang='fr', gender="female"):
    cle = "4c9e5aae707e41518A148720a8b56c11"
    region = "francecentral"
    speech_config = speechsdk.SpeechConfig(subscription=cle, region=region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    #speech_config.speech_synthesis_voice_name = 'fr-FR-CelesteNeural'
    speech_config.speech_synthesis_voice_name = Speaker_Choice(gender=gender, language=lang)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

def Speech_To_Text2(speech_audio): 
    # load Model and audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(speech_audio)
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    print("Detected language:", detected_language)

    # decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    return result.text, detected_language

def Speech_To_Text(filepath,spoken_language="en-US"):
    # Set Configs
    cle = "4c9e5aae707e41518A148720a8b56c11"
    region = "francecentral"
    speech_config = speechsdk.SpeechConfig(subscription=cle, region=region)
    speech_config.speech_recognition_language=spoken_language
    audio_input = speechsdk.AudioConfig(filename=filepath)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    # Get Result
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return f"No speech could be recognised: {speech_recognition_result.no_match_details}"
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        error_msg = f"Speech Recognition canceled: {cancellation_details.reason}"
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            error_msg += "\n" + f"Error details: {cancellation_details.error_details}"
        return error_msg

def save_latex(latex):
  with open("static/latex.txt","w",encoding='utf-8') as f:
    f.write(latex)

def simplify_multiplication(match_obj):
    if match_obj.group() is not None:
        to_change = match_obj.group()
        return to_change[:-1] + " times " + to_change[-1]

def RegEx(text):
  # Clean the Text (get of last '.' and useless characters ',')
  text = text[:-1].replace(',', '') if text[-1] == "." else text.replace(',', '')
  # ax => a times x
  text = re.sub("\d+[a-z]+", simplify_multiplication, text) 
  # Simplify Power: x^4 = superscript 4 -> x power 4
  text = text.replace("power", "superscript")
  return text

def Latex_To_Text(latex):
  # Make Latex format more understandable (regex)
  latex = latex.replace(f"\r", f'\\r')
  text = LatexNodes2Text().latex_to_text(latex)
  return text

def Text_To_Latex(text):
    matplotlib.use('Agg')
    saytex_compiler = Saytex()
    try:
      text = RegEx(text)
      latex_result = saytex_compiler.to_latex(text)
      save_latex(latex_result)
      
    except:
      latex_result = "Error: Text Not Recognized in Latex"
    # Display Graph
    left, width, bottom, height = .30, .4, .25, .6; right = left + width; top = bottom + height
    fig = plt.figure()
    fontsize = 75 if len(text.split(" ")) < 30 else 20
    plt.text(0.5 *(left+right), 0.5*(bottom+top), "$"+ latex_result + "$", horizontalalignment='center', verticalalignment='center', fontsize=fontsize) # r"$%s$" % latex_result
    plt.axis('off')
    return latex_result, fig

app = Flask(__name__)

transcript = ""
@app.route('/', methods=['GET','POST'])
def main(): 
  transcript = ""
  with open("static/latex.txt","r") as f:
    latex = f.read()

  with open("static/old_latex.txt","r") as f2:
    old_latex = f2.readlines()

  images = ["static/images/latex_fig/"+ i for i in os.listdir("static/images/latex_fig")[:-1]]
  if request.method == 'POST':
    if "audio-file" in request.files:
      f = request.files["audio-file"]
      segment = AudioSegment.from_file(f.stream)
      segment.export("static/audio/sam.wav", format="wav")

      try:
        transcript,lang = Speech_To_Text2("static/audio/sam.wav")
        latex,fig = Text_To_Latex(transcript)
        image_path = "static/images/latex_fig/test.png"
        fig.savefig(image_path)
      except:
        print("Erreur de conversion Audio")

      print(transcript)
      return redirect(url_for("main"))
    else:
      with open("static/latex.txt","r",encoding='utf-8') as f:
        latex_text = f.read()
      text2speech(text_to_readable(Latex_To_Text(latex_text)))
      return redirect(url_for("main"))
  else:
    return render_template('main.html',transcript=transcript,old_latex=old_latex,latex=latex,images=images)

@app.route('/listening', methods=['GET','POST'])
def listen():
    # latex,fig = Text_To_Latex("x squared plus 5")

    image_path = "static/images/latex_fig/test.png"
    # fig.savefig(image_path)
    return render_template('main.html',message="test",image_path=image_path)

@app.route('/save_current_to_historic', methods=['GET','POST'])
def save_to_historic():
  if request.method == 'POST':
    current = request.form["current_value"]
  
  images = os.listdir("static/images/latex_fig")
  image_historique = "image_"+ str(len(images)-1) +".png"

  shutil.copy("static/images/latex_fig/test.png", "static/images/latex_fig/"+image_historique)

  with open("static/old_latex.txt","r") as f:
    historic = f.read()

  with open("static/old_latex.txt","w") as f:
    f.write(historic+"\n"+Latex_To_Text(current))
  return redirect(url_for("main"))

@app.route('/clear_historic', methods=['GET','POST'])
def clear_historic():
  if request.method == 'POST':
    with open("static/old_latex.txt","w",encoding='utf-8') as f:
      f.write("")
    for file in os.listdir("static/images/latex_fig/"):
      if file.startswith("image_"):
        os.remove("static/images/latex_fig/"+file)
  return redirect(url_for("main"))

@app.route('/test', methods=['GET','POST'])
def test(): 
  if request.method == 'POST':
    return render_template("test.html")
  return render_template('test.html')

if __name__ == '__main__':
    load_model()
    app.run(debug = True)