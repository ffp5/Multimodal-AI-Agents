from flask import Flask, request, jsonify
from backend.agents.agent import OpenAIAgent
from backend.tools.hotel import HotelTool
from backend.tools.final_return import ReturnTool
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def create_agent():
    use_gemini = True
    return OpenAIAgent(
        name="Road trip planner",
        tools=[
            HotelTool(),
            ReturnTool()
        ],
        api_key=os.environ["GEMINI_API_KEY"] if use_gemini else os.environ["API_KEY_OPENAI"],
        model="gemini-2.0-flash" if use_gemini else "gpt-4",
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

if __name__ == '__main__':
    app.run(debug=True)
