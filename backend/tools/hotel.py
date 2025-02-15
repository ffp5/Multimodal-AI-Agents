from tools.base_tool import BaseTool
from tools.base_tool import ToolParameter
from tools.base_tool import ParameterType
from typing import List, Dict, Any
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HotelTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="hotel searcher",
            description="Recherche d'hôtels sur Booking.com et renvoie les n premiers résultats",
        )

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="location",
                param_type=ParameterType.STRING,
                description="Loalisation de l'hôtel",
                required=True
            ),
            ToolParameter(
                name="nb_results",
                param_type=ParameterType.INTEGER,
                description="Nombre de résultats à renvoyer",
                required=False,
            )
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        # Convertir les paramètres en float si nécessaire
        try:
            location = kwargs["location"]
            nb_results = int(kwargs.get("nb_results", 5))
            url = "https://places.googleapis.com/v1/places:searchNearby"

            payload = {
                "includedTypes": ["restaurant"],  # Can be changed to other types
                "maxResultCount": 3,
                "locationRestriction": {
                    "circle": {
                        "center": {"latitude": 48.8566, "longitude": 2.3522},  # Paris coordinates
                        "radius": 500.0  # Radius in meters
                    }
                }
            }

            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": os.getenv('GOOGLE_API_KEY'),
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress"  # Specify needed fields
            }



            #TODO: Rechercher les hôtels


            return {"result": f"Recherche d'hôtels à {location} (nombre de résultats: {nb_results})"}
        except (ValueError, TypeError) as e:
            return {"error": f"Erreur de conversion des nombres: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}
