import os
from pydub import AudioSegment

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

import pandas as pd


from saytex import Saytex 

import matplotlib
import matplotlib.pyplot as plt
# Converts Text into Latex using the "Saytex" Library (also returns a the eq as a plot)
def Text_To_Latex(text):
    matplotlib.use('Agg')
    saytex_compiler = Saytex()
    try:
      latex_result = saytex_compiler.to_latex(text)
    except:
      latex_result = "Error: Text Not Recognized in Latex"
    # Display Graph
    left, width, bottom, height = .25, .5, .25, .5; right = left + width; top = bottom + height
    fig = plt.figure()
    fontsize = 24 if len(text.split(" ")) < 30 else 20
    plt.text(0.5 *(left+right), 0.5*(bottom+top), "$"+ latex_result + "$", horizontalalignment='center', verticalalignment='center', fontsize=fontsize) # r"$%s$" % latex_result
    plt.axis('off')
    return latex_result, fig

app = Flask(__name__)

@app.route('/')
def main(): 
    return render_template('main.html')

@app.route('/listening', methods=['POST'])
def listen():
    latex,fig = Text_To_Latex("x squared plus 5")

    image_path = "static/images/latex_fig/test.png"
    fig.savefig(image_path)
    return render_template('main.html',message=latex,image_path=image_path)

@app.route('/audioUpload', methods=['POST'])
def audio():
  if request.method == 'POST':

    import speech_recognition as sr
    r = sr.Recognizer()
    
    with open("static/audio/test.mp3","wb") as ifile:
      ifile.write(request.files["audio-file"].stream.read())

    sound = AudioSegment.from_mp3("static/audio/test.mp3")
    sound.export("static/audio/test.wav", format="wav")
    with sr.AudioFile('static/audio/test.wav') as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
        except:
            print('Sorry.. run again...')
  return render_template('main.html')


if __name__ == '__main__':
    app.run(debug = True)