from cgitb import text
from distutils.log import debug
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
# import string
import json
import convertation as cv
import re
import unidecode

chatbot = ChatBot("Max")

preguntas = []
# Función que carga las preguntas anteriores desde el JSON
def cargar_preguntas():
    try:
        with open('preguntas_no_respondidas.json', 'r') as file:
            preguntas = json.load(file)
    except FileNotFoundError:
        preguntas = []
    return preguntas

# Función que guarda las preguntas no respondidas en el JSON
def guardar_preguntas(preguntas):
    with open('preguntas_no_respondidas.json', 'w') as file:
        json.dump(preguntas, file)

# Función que procesa la pregunta antes de ingresarla convirtiendo a minúscula y quitando los signos de puntuación
def procesar_pregunta(texto):
    texto = texto.lower()
    #eliminando todos los signos menos los acentos
    texto_sin_signos = re.sub(r'[^\w\s]','', texto)
    #eliminando los acentos
    texto_sin_acentos = unidecode.unidecode(texto_sin_signos)
    #eliminando el ultimo espacio si lo tienen
    texto_sin_espacios = texto_sin_acentos.rstrip()
    # print(texto_sin_espacios)
    return texto_sin_espacios

# Inicializando y entrenando el bot
trainer = ListTrainer(chatbot)
trainer.train(cv.conversation)


app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    # Lógica para procesar la solicitud POST
    data = request.get_json()
    user_input = data['input']
    pre = procesar_pregunta(user_input)
    response = chatbot.get_response(pre)
    # print(pregunta)
    no_entendido = 'No entiendo tu pregunta'
    if response.confidence < 0.5:
        preguntas.append(pre)
        guardar_preguntas(preguntas)
        return jsonify({'response': str(no_entendido)})
    else:
        return jsonify({'response': str(response)})

# Ruta de bienvenida
@app.route('/')
def welcome():
    return '¡Hola, soy HydroBot!'

@app.route('/preguntas')
def obtener_preguntas():
    return jsonify({'preguntas': preguntas})

@app.before_request
def guardar_preguntas_sqlite():
    guardar_preguntas(preguntas)  # Guardar las preguntas no respondidas en la base de datos SQLite antes de cada solicitud

if __name__ == '__main__':
    # Cargando las preguntas no respondidas desde JSON
    preguntas = cargar_preguntas()

    app.run()
