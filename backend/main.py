import logging

from backend.agents.agent import OpenAIAgent
from backend.tools.hotel import HotelTool
from backend.tools.maps import MapsTool
from backend.tools.final_return import ReturnTool
from backend.tools.maps_openstreetmap import OpenStreetMapTool
from backend.tools.hotel_open import HotelToolOpen

import os
from colorama import init, Fore, Style
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

# Initialisation de colorama
init()

use_gemini = False

# Création des callbacks
def on_message(message):
    color = Fore.GREEN if message.role == "assistant" else Fore.BLUE if message.role == "user" else Fore.YELLOW
    print(f"{color}[{message.role}]: {message.content}{Style.RESET_ALL}")

def on_tool_use(tool_call):
    print(f"{Fore.CYAN}Utilisation de l'outil: {tool_call.tool_name} avec les arguments {tool_call.parameters}{Style.RESET_ALL}")

# Initialisation de l'agent
agent = OpenAIAgent(
    name="Road trip planner",
    tools=[
        HotelToolOpen(),
        OpenStreetMapTool(),
        ReturnTool()
    ],
    api_key=os.environ["GEMINI_API_KEY"] if use_gemini else os.environ["API_KEY_OPENAI"],
    model="gemini-2.0-pro-exp-02-05" if use_gemini else "gpt-4o",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" if use_gemini else None,
    on_message=on_message,
    on_tool_use=on_tool_use
)

# Exécution d'une tâcxhe
result = agent.execute_task("Plannifier un road trip de 5 jours en France, en visitant Paris, Lyon et Marseille. Et trouve moi des hôtels pour chaque étape. Utilise les outils si nécessaire.")