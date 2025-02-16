from flask import Flask, request, jsonify, Response
from flasgger import Swagger
from backend.agents.agent import OpenAIAgent, Message, ToolCall
from backend.tools.hotel_open import HotelToolOpen
from backend.tools.maps_openstreetmap import OpenStreetMapTool
from backend.tools.final_return import ReturnTool
from backend.config.swagger_config import template, swagger_config
import os
from dotenv import load_dotenv
import json
from flask_cors import CORS


load_dotenv()
app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template=template, config=swagger_config)

def create_agent():
    use_gemini = True
    return OpenAIAgent(
        name="Road trip planner",
        tools=[
            HotelToolOpen(),
            OpenStreetMapTool(),
            ReturnTool()
        ],
        api_key=os.environ["GEMINI_API_KEY"] if use_gemini else os.environ["API_KEY_OPENAI"],
        model="gemini-2.0-flash" if use_gemini else "gpt-4o",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/" if use_gemini else None
    )

def create_streaming_agent():
    use_gemini = False
    return OpenAIAgent(
        name="Road trip planner",
        tools=[
            HotelToolOpen(),
            OpenStreetMapTool(),
            ReturnTool()
        ],
        api_key=os.environ["GEMINI_API_KEY"] if use_gemini else os.environ["API_KEY_OPENAI"],
        model="gemini-2.0-flash" if use_gemini else "gpt-4o",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/" if use_gemini else None
    )

@app.route('/', methods=['GET'])
def home():
    """Page d'accueil de l'API
    ---
    responses:
      200:
        description: Message de bienvenue
    """
    return jsonify({'message': 'Bienvenue sur l\'API de planification de road trip'}), 200

@app.route('/plan-trip', methods=['POST'])
def plan_trip():
    """Planifie un road trip avec des étapes et des hôtels
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - start_location
            - end_location
            - duration
          properties:
            start_location:
              type: string
              description: Ville de départ
            end_location:
              type: string
              description: Ville d'arrivée
            duration:
              type: integer
              description: Durée du voyage en jours
    responses:
      200:
        description: Plan de voyage généré avec succès
      400:
        description: Paramètres manquants ou invalides
      500:
        description: Erreur serveur
    """
    data = request.get_json()
    
    # Validation des paramètres requis
    required_params = ['start_location', 'end_location', 'duration']
    if not all(param in data for param in required_params):
        return jsonify({
            'error': 'Missing required parameters. Please provide start_location, end_location, and duration'
        }), 400
    
    try:
        duration = int(data['duration'])
    except ValueError:
        return jsonify({'error': 'Duration must be a number'}), 400

    # Création de l'agent et exécution de la tâche
    agent = create_agent()
    prompt = f"Planifier un road trip de {duration} jours en France, en partant de {data['start_location']} pour aller à {data['end_location']}. Trouve des hôtels pour chaque étape."
    
    try:
        result = agent.execute_task(prompt)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/plan-trip-stream', methods=['POST'])
def plan_trip_stream():
    """Planifie un road trip avec des étapes et des hôtels (version streaming)
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - start_location
            - end_location
            - duration
          properties:
            start_location:
              type: string
              description: Ville de départ
            end_location:
              type: string
              description: Ville d'arrivée
            duration:
              type: integer
              description: Durée du voyage en jours
    responses:
      200:
        description: Stream d'événements contenant les mises à jour en temps réel
      400:
        description: Paramètres manquants ou invalides
    """
    data = request.get_json()
    
    # Validation des paramètres requis
    required_params = ['start_location', 'end_location', 'duration']
    if not all(param in data for param in required_params):
        return jsonify({
            'error': 'Missing required parameters'
        }), 400
    
    try:
        duration = int(data['duration'])
    except ValueError:
        return jsonify({'error': 'Duration must be a number'}), 400

    def generate():
        agent = create_streaming_agent()
        prompt = f"Planifier un road trip de {duration} jours en France, en partant de {data['start_location']} pour aller à {data['end_location']}. Trouve des hôtels pour chaque étape."
        
        try:
            for event in agent.execute_task(prompt):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': {'message': str(e)}})}\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
