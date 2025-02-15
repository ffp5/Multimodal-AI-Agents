from agents.agent import OpenAIAgent
from tools.calculator import CalculatorTool
import os
from colorama import init, Fore, Style

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
    name="mon_agent",
    tools=[
        CalculatorTool(),
        StopTool(),
        TerminalTool(),
        FileTreeTool(),
        FileReaderTool(),
        PythonExecutorTool(),
        FileWriterTool(),
        UserInputTool()
    ],
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-4o",
    on_message=on_message,
    on_tool_use=on_tool_use
)

# Exécution d'une tâche
result = agent.execute_task("Créer moi un site web en flask.")