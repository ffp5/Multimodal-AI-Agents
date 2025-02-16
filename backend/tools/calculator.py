from backend.tools.base_tool import BaseTool
from backend.tools.base_tool import ToolParameter
from backend.tools.base_tool import ParameterType
from typing import List, Dict, Any

class CalculatorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Outil de calcul"
        )

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="x",
                param_type=ParameterType.FLOAT,
                description="Premier nombre",
                required=True
            ),
            ToolParameter(
                name="y",
                param_type=ParameterType.FLOAT,
                description="Deuxième nombre",
                required=True,
            )
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        # Convertir les paramètres en float si nécessaire
        try:
            x = float(kwargs["x"])
            y = float(kwargs["y"])
            result = x + y
            return {"result": result}
        except (ValueError, TypeError) as e:
            return {"error": f"Erreur de conversion des nombres: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}
