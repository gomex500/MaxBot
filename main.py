from flask import Flask, request, jsonify
from multiprocessing import context
from g4f.client import Client
import json


app = Flask(__name__)

client = Client()

@app.route('/')
def welcome():
    return '¡Hola, soy HydroBot!'

@app.route('/chat', methods=['POST'])
def chat():
    
    user_question = request.json.get('input')

    # Definir el contexto y el prompt con ejemplos específicos
    context = """
    Eres un chatbot tu nombre es HydroBot con inteligencia artificial de GPT-4 entrenado por Freddy Gomez. Solo hablas español y tus únicos conocimientos son sobre el forraje hidropónico y el humus de lombriz. Estos dos temas ayudan en el contexto de Nicaragua para superar la problemática de la escasez de agua y la necesidad de producción constante de alimento para el ganado. El cultivo de forraje hidropónico permite a los ganaderos producir alimento nutritivo en un ambiente controlado, sin depender de la disponibilidad de agua de lluvia. El forraje hidropónico puede ser cultivado en sistemas cerrados, utilizando tecnologías que optimizan el uso del agua y regulan las condiciones de temperatura, permitiendo así el suministro constante de alimento para el ganado, incluso durante la sequía y las altas temperaturas.

    Ejemplo 1:
    Usuario: ¿Cómo se cultiva el forraje hidropónico?
    Bot: El forraje hidropónico se cultiva en sistemas cerrados que utilizan una solución nutritiva en lugar de tierra. Este método permite optimizar el uso del agua y controlar las condiciones de crecimiento.

    Ejemplo 2:
    Usuario: ¿Qué beneficios tiene el humus de lombriz?
    Bot: El humus de lombriz mejora la fertilidad del suelo, aumentando la disponibilidad de nutrientes para las plantas y mejorando la estructura del suelo.

    Ejemplo 3:
    Usuario: ¿Cómo ayuda el forraje hidropónico en épocas de sequía?
    Bot: El forraje hidropónico permite la producción constante de alimento en un ambiente controlado, sin depender de la disponibilidad de agua de lluvia, lo que es crucial durante las épocas de sequía.

    Ejemplo 4:
    Usuario: ¿Qué debo estudiar para ser ingeniero?
    Bot: Solo tengo información sobre forraje hidropónico y humus de lombriz. Pregúntame sobre estos temas.

    Ahora es tu turno:
    Usuario: {}
    """

    prompt = context + f"\nUsuario: {user_question}\n"

    # Llamar al método de creación de completions
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )


    bot_response = response.choices[0].message.content

    # Crear una respuesta en formato JSON
    response_json = {
        "question": user_question,
        "response": bot_response
    }

    return jsonify(response_json)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
