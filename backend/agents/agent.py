from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json, os
import logging
from openai import OpenAI
from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from backend.agents.system_prompt import system_prompt

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
        max_history: int = 1000,
        temperature: float = 0.7,
        on_message: Optional[Callable[[Message], None]] = None,
        on_tool_use: Optional[Callable[[ToolCall], None]] = None
    ):
        self.name = name
        self.tools = {tool.name: tool for tool in tools}
        self.max_history = max_history
        self.conversation_history: List[Message] = []
        self.tool_calls_history: List[ToolCall] = []
        
        # Configuration Gemini
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = model
        self.temperature = temperature
        
        # Callbacks pour le suivi en temps réel
        self.on_message = on_message
        self.on_tool_use = on_tool_use
        
        # Configuration du logging
        self.logger = logging.getLogger(f"agent.{name}")
        self.logger.setLevel(logging.INFO)

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
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        if self.on_message:
            self.on_message(message)

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        """Retourne le schéma des outils au format OpenAI"""
        return [tool.get_schema() for tool in self.tools]

    def execute_task(self, task_description: str, max_steps: int = 10) -> Dict[str, Any]:
        self.logger.info(f"Démarrage de la tâche: {task_description}")
        
        # Message initial avec instructions simplifiées
        system_message = Message(
            role="system",
            content=system_prompt)
        
        user_message = Message(
            role="user",
            content=task_description
        )
        
        messages = [system_message, user_message]
        self._add_to_history(system_message)
        self._add_to_history(user_message)
        
        step = 0
        while step < max_steps:
            step += 1
            self.logger.info(f"Étape {step}/{max_steps}")
            
            try:
                # Création du message pour l'API
                api_messages = [
                    {
                        "role": msg.role, 
                        "content": msg.content,
                        **({"name": msg.name} if msg.name else {}),
                        **({"tool_call_id": msg.tool_call_id} if msg.tool_call_id else {})
                    }
                    for msg in messages
                ]
                
                # Appel à l'API OpenAI
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=api_messages,
                    tools=[tool.get_schema() for tool in self.tools.values()],
                    tool_choice="auto",
                    temperature=self.temperature
                )
                
                # Traitement de la réponse
                assistant_message = response.choices[0].message
                
                # Créer le message de l'assistant avec son contenu explicatif
                if assistant_message.content:
                    explain_msg = Message(
                        role="assistant",
                        content=assistant_message.content
                    )
                    messages.append(explain_msg)
                    self._add_to_history(explain_msg)
                
                # Gestion des appels d'outils si présents
                if assistant_message.tool_calls:
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        
                        # Afficher le message de contexte pour l'utilisation de l'outil
                        if self.on_message:
                            context_msg = Message(
                                role="tool_context",
                                content=f"Je vais utiliser l'outil {tool_name} avec les paramètres : {tool_args}"
                            )
                            self._add_to_history(context_msg)
                        
                        tool_call_record = ToolCall(
                            tool_name=tool_name,
                            parameters=tool_args
                        )
                        
                        try:
                            # Exécution de l'outil
                            result = self.tools[tool_name].execute(**tool_args)
                            tool_call_record.response = result
                            
                            # Ajout du message avec l'appel d'outil et sa réponse
                            tool_msg = Message(
                                role="function",
                                content=json.dumps(result),
                                name=tool_name,
                                tool_call_id=tool_call.id
                            )
                            messages.append(tool_msg)
                            self._add_to_history(tool_msg)
                            
                            if tool_name == "return":
                                # Si c'est un appel direct à return, sortir de la boucle
                                return {
                                    "steps_taken": step,
                                    "conversation": self.conversation_history,
                                    "tool_calls": self.tool_calls_history,
                                    "result": result
                                }
                            
                        except Exception as e:
                            error_msg = str(e)
                            tool_call_record.error = error_msg
                            self.logger.error(f"Erreur d'exécution de l'outil: {error_msg}")
                        
                        if self.on_tool_use:
                            self.on_tool_use(tool_call_record)
                        
                        self.tool_calls_history.append(tool_call_record)
                
                # La vérification de fin de tâche n'est plus nécessaire ici
                # car nous retournons directement après stop
                
            except Exception as e:
                self.logger.error(f"Erreur lors de l'exécution: {str(e)}")
                raise
        
        return {
            "steps_taken": step,
            "conversation": self.conversation_history,
            "tool_calls": self.tool_calls_history
        }