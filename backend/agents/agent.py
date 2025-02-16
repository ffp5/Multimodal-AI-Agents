from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json, os
import logging
from openai import OpenAI
from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from backend.agents.system_prompt import system_prompt_road_trip_planner
import traceback
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

@dataclass
class Message:
    role: str
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

@dataclass
class ToolCall:
    tool_name: str
    parameters: Dict[str, Any]
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class OpenAIAgent:
    def __init__(
        self,
        name: str,
        tools: List[Any],
        api_key: str,
        model: str = "gemini-2.0-flash",
        base_url: str = "https://api.openai.com/v1",
        temperature: float = 0.7,
        on_message: Optional[Callable[[Message], None]] = None,
        on_tool_use: Optional[Callable[[ToolCall], None]] = None
    ):
        self.console = Console()
        self.name = name
        self.tools = {tool.name: tool for tool in tools}
        self.conversation_history: List[Message] = []
        self.tool_calls_history: List[ToolCall] = []
        
        # Configuration Gemini
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.temperature = temperature
        
        # Callbacks pour le suivi en temps réel
        self.on_message = on_message
        self.on_tool_use = on_tool_use
        
        # Configuration du logging améliorée
        self.logger = logging.getLogger(f"agent.{name}")
        self.logger.setLevel(logging.INFO)
        
        # Ajout d'un handler console si aucun n'existe
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        self.logger.debug(f"Agent {name} initialisé avec le modèle {model}")
        self.console.print(f"[bold green]Agent {name} initialisé avec le modèle {model}[/bold green]")

    def _create_tools_description(self) -> List[Dict[str, Any]]:
        """Crée la description des outils pour l'API OpenAI"""
        # Mapping des types pour JSON Schema
        type_mapping = {
            ParameterType.STRING: "string",
            ParameterType.INTEGER: "integer",
            ParameterType.FLOAT: "number",
            ParameterType.BOOLEAN: "boolean",
            ParameterType.LIST: "array",
            ParameterType.DICT: "object"
        }

        tools = []
        for tool in self.tools.values():
            tool_desc = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            
            # Ajout des paramètres
            for param in tool.parameters:
                tool_desc["function"]["parameters"]["properties"][param.name] = {
                    "type": type_mapping[param.param_type],
                    "description": param.description
                }
                if param.constraints:
                    if "choices" in param.constraints:
                        tool_desc["function"]["parameters"]["properties"][param.name]["enum"] = \
                            param.constraints["choices"]
                if param.required:
                    tool_desc["function"]["parameters"]["required"].append(param.name)
            
            tools.append(tool_desc)
        
        return tools

    def _add_to_history(self, message: Message):
        """Ajoute un message à l'historique"""
        self.conversation_history.append(message)
        
        if self.on_message:
            self.on_message(message)

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Retourne le schéma des outils au format OpenAI"""
        return [tool.get_schema() for tool in self.tools]

    def execute_task(self, task_description: str, max_steps: int = 10):
        self.console.print(Panel(f"[bold blue]Nouvelle tâche[/bold blue]\n{task_description}"))
        
        self.logger.debug(f"Démarrage de la tâche: {task_description}")
        
        system_message = Message(
            role="system",
            content=system_prompt_road_trip_planner
        )
        user_message = Message(
            role="user",
            content=task_description
        )
        
        messages = [system_message, user_message]
        
        # Yield initial messages
        yield {
            'type': 'message',
            'data': system_message.__dict__
        }
        yield {
            'type': 'message',
            'data': user_message.__dict__
        }
        
        step = 0
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Traitement en cours...", total=max_steps)
            
            while step < max_steps:
                step += 1
                progress.update(task, advance=1, description=f"[cyan]Étape {step}/{max_steps}")
                
                try:
                    api_messages = [
                        {
                            "role": msg.role, 
                            "content": msg.content,
                            **({"name": msg.name} if msg.name else {}),
                            **({"tool_call_id": msg.tool_call_id} if msg.tool_call_id else {})
                        }
                        for msg in messages
                    ]
                    
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=api_messages,
                        tools=[tool.get_schema() for tool in self.tools.values()],
                        tool_choice="auto",
                        temperature=self.temperature
                    )

                    assistant_message = response.choices[0].message
                    
                    # Créer un Message à partir de la réponse de l'assistant
                    assistant_msg = Message(
                        role="assistant",
                        content=assistant_message.content if assistant_message.content else ""
                    )
                    messages.append(assistant_msg)
                    
                    # Yield assistant's response
                    yield {
                        'type': 'message',
                        'data': assistant_msg.__dict__
                    }
                    
                    if assistant_message.content:
                        self.console.print(Panel(
                            assistant_message.content,
                            title="[bold purple]Assistant[/bold purple]",
                            border_style="purple"
                        ))
                    
                    if assistant_message.tool_calls:
                        for tool_call in assistant_message.tool_calls:
                            tool_name = tool_call.function.name
                            tool_args = json.loads(tool_call.function.arguments)
                            
                            self.console.print(f"[bold yellow]Utilisation de l'outil[/bold yellow]: {tool_name}")
                            self.console.print(f"[dim]Paramètres:[/dim] {tool_args}")
                            
                            # Yield tool call event
                            yield {
                                'type': 'tool_call',
                                'data': {
                                    'tool_name': tool_name,
                                    'parameters': tool_args
                                }
                            }

                            try:
                                result = self.tools[tool_name].execute(**tool_args)

                                self.console.print(f"[bold green]Résultat de l'outil {tool_name}:[/bold green]")
                                self.console.print(Panel(str(result), style="green"))
                                
                                """"
                                # Convertir le générateur en liste si nécessaire
                                if hasattr(result, '__iter__') and hasattr(result, '__next__'):
                                    result = list(result)"""
                                
                                # Yield tool result
                                yield {
                                    'type': 'tool_result',
                                    'data': {
                                        'tool_name': tool_name,
                                        'result': result
                                    }
                                }

                                if tool_name == "return":
                                    result = result
                                    yield {
                                        'type': 'final_result',
                                        'data': result["result"]
                                    }
                                    self.console.print("[bold green]✓ Tâche terminée avec succès![/bold green]")
                                    step = max_steps # Terminer la boucle

                                # Créer un Message pour la réponse de l'outil
                                tool_msg = Message(
                                    role="function",
                                    name=tool_name,
                                    content=json.dumps(result)
                                )
                                messages.append(tool_msg)



                            except Exception as e:
                                self.console.print(f"[bold red]Erreur lors de l'exécution de l'outil {tool_name}:[/bold red]")
                                self.console.print(Panel(str(e), style="red"))
                                print(e)
                                traceback.print_exc()
                                yield {
                                    'type': 'error',
                                    'data': {
                                        'message': str(e)
                                    }
                                }
                                raise


                except Exception as e:
                    self.console.print("[bold red]Erreur générale:[/bold red]")
                    self.console.print(Panel(str(e), style="red"))
                    print(e)
                    traceback.print_exc()
                    yield {
                        'type': 'error',
                        'data': {
                            'message': str(e)
                        }
                    }
                    raise