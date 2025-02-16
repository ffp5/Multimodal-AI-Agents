from flask import Flask, request, jsonify, Response
from backend.agents.agent import OpenAIAgent, Message, ToolCall
from backend.tools.hotel_open import HotelToolOpen
from backend.tools.maps_openstreetmap import OpenStreetMapTool
from backend.tools.final_return import ReturnTool
import os
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

def create_agent():
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

@app.route('/plan-trip', methods=['POST'])
def plan_trip():
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
    app.run(debug=True)
