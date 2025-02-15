from tools.base_tool import BaseTool, ToolParameter, ParameterType
from agents.system_prompt import json_output

class ReturnTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="return",
            description="Outil pour terminer la conversation, et renvoyer tes résultats",
        )

    def _define_parameters(self):
        return [
            ToolParameter(
                name="result",
                param_type=ParameterType.STRING,
                description="Retourne lse infromations sous ce format :\n\n" + json_output["output"],
                required=True,
            )
        ]

    def execute(self, reason: str = "Conversation terminée") -> dict:
        return {
            "status": "stopped",
            "reason": reason
        }
