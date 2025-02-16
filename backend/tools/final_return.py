from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from backend.agents.system_prompt import dict_output
import json

json_output = json.dumps(dict_output, indent=4, ensure_ascii=False)

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
                description="Retourne les infromations sous ce format :\n\n" + json_output,
                required=True,
            )
        ]

    def execute(self, result: str) -> dict:
        # On convertit la réponse du llm en json
        try:
            result_json = json.loads(result)
        except Exception as e:
            raise ValueError(f"Erreur lors de la conversion de la réponse en JSON : {e}")

        return {
            "result": result_json,
        }
