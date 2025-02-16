from flask import Flask, request, jsonify, Response
from flasgger import Swagger
from backend.agents.agent import OpenAIAgent, Message, ToolCall
from backend.tools.hotel_open import HotelToolOpen
from backend.tools.maps_openstreetmap import OpenStreetMapTool
from backend.tools.final_return import ReturnTool
from backend.config.swagger_config import template, swagger_config
import os
import weave
from dotenv import load_dotenv
import json
from flask_cors import CORS


load_dotenv()
app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template=template, config=swagger_config)

weave.init("roadtrip-planner")

@weave.op()
def create_streaming_agent():
    use_together = True
    return OpenAIAgent(
        name="Road trip planner",
        tools=[
            HotelToolOpen(),
            OpenStreetMapTool(),
            ReturnTool()
        ],
        api_key=os.environ["TOGETHER_API_KEY"] if use_together else os.environ["API_KEY_OPENAI"],
        model="deepseek-ai/DeepSeek-V3" if use_together else "gpt-4o",
        base_url="https://api.together.xyz/v1/chat/completions" if use_together else None
    )

@weave.op()
def process_trip_request(data):
    agent = create_streaming_agent()
    prompt = f"Plan a {data['duration']} day road trip from {data['start_location']} to {data['end_location']}. Find hotels for each stop."
    return agent.execute_task(prompt)

@app.route('/', methods=['GET'])
def home():
    """Page d'accueil de l'API
    ---
    responses:
      200:
        description: Message de bienvenue
    """
    return jsonify({'message': 'Bienvenue sur l\'API de planification de road trip'}), 200

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
        try:
            for event in process_trip_request(data):
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
