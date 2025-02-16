from backend.agents.agent import OpenAIAgent
from backend.tools.hotel import HotelTool
from backend.tools.maps import MapsTool
from backend.tools.final_return import ReturnTool

import os
from colorama import init, Fore, Style
from dotenv import load_dotenv

load_dotenv()

# Initialisation de colorama
init()

# Création des callbacks
def on_message(message):
    color = Fore.GREEN if message.role == "assistant" else Fore.BLUE if message.role == "user" else Fore.YELLOW
    print(f"{color}[{message.role}]: {message.content}{Style.RESET_ALL}")

def on_tool_use(tool_call):
    print(f"{Fore.CYAN}Utilisation de l'outil: {tool_call.tool_name}{Style.RESET_ALL}")

# Initialisation de l'agent
agent = OpenAIAgent(
    name="Road trip planner",
    tools=[
        #HotelTool(),
        #MapsTool(),
        ReturnTool()
    ],
    api_key=os.environ["GOOGLE_API_KEY"],
    model="gemini-2.0-flash",
    on_message=on_message,
    on_tool_use=on_tool_use
)

# Exécution d'une tâche
result = agent.execute_task("Créer moi un site web en flask.")