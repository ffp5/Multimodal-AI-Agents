from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Définition des types de paramètres
class ParameterType(Enum):
    STRING = {
        "type": "string"
    }
    INTEGER = {
        "type": "integer"
    }
    FLOAT = {
        "type": "number"
    }
    BOOLEAN = {
        "type": "boolean"
    }
    LIST = {
        "type": "array",
        "items": {
            "type": "string",
            "description": "Élément de la liste"
        }
    }
    DICT = {
        "type": "object"
    }

@dataclass
class ToolParameter:
    name: str
    param_type: ParameterType
    description: str
    required: bool = True
    default: Any = None
    constraints: Optional[Dict[str, Any]] = None

class BaseTool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters: List[ToolParameter] = self._define_parameters()

    @abstractmethod
    def _define_parameters(self) -> List[ToolParameter]:
        """Définit les paramètres requis pour l'outil"""
        pass

    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Valide les paramètres fournis"""
        for param in self.parameters:
            # Vérifier si les paramètres requis sont présents
            if param.required and param.name not in params:
                raise ValueError(f"Paramètre requis manquant: {param.name}")
            
            # Vérifier le type si le paramètre est fourni
            if param.name in params:
                value = params[param.name]
                if not self._check_type(value, param.param_type):
                    raise TypeError(f"Type invalide pour {param.name}. Attendu: {param.param_type.value}")
                
                # Vérifier les contraintes si définies
                if param.constraints:
                    self._validate_constraints(param, value)
        
        return True

    def _check_type(self, value: Any, expected_type: ParameterType) -> bool:
        type_mapping = {
            ParameterType.STRING: str,
            ParameterType.INTEGER: int,
            ParameterType.FLOAT: (int, float),
            ParameterType.BOOLEAN: bool,
            ParameterType.LIST: list,
            ParameterType.DICT: dict
        }
        return isinstance(value, type_mapping[expected_type])

    def _validate_constraints(self, param: ToolParameter, value: Any):
        if not param.constraints:
            return True
        
        for constraint, constraint_value in param.constraints.items():
            if constraint == "min":
                if value < constraint_value:
                    raise ValueError(f"{param.name} doit être >= {constraint_value}")
            elif constraint == "max":
                if value > constraint_value:
                    raise ValueError(f"{param.name} doit être <= {constraint_value}")
            elif constraint == "choices":
                if value not in constraint_value:
                    raise ValueError(f"{param.name} doit être parmi {constraint_value}")

    def get_schema(self) -> Dict[str, Any]:
        """Génère le schéma OpenAI pour l'outil"""
        properties = {}
        required = []
        
        for param in self.parameters:
            if isinstance(param.param_type.value, dict):
                schema = param.param_type.value.copy()
            else:
                # Cas spécial pour les types simples
                schema = {"type": param.param_type.value}
            
            schema["description"] = param.description
            
            if param.constraints:
                if "min" in param.constraints:
                    schema["minimum"] = param.constraints["min"]
                if "max" in param.constraints:
                    schema["maximum"] = param.constraints["max"]
                if "choices" in param.constraints:
                    schema["enum"] = param.constraints["choices"]
            
            properties[param.name] = schema
            
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Exécute l'outil avec les paramètres validés"""
        pass
