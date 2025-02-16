from backend.tools.base_tool import BaseTool
from backend.tools.base_tool import ToolParameter
from backend.tools.base_tool import ParameterType
from typing import List, Dict, Any
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ActivityTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="activity searcher",
            description="Recherche les activités dans le coin",
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
            
             # Get location coordinates
            url = "https://places.googleapis.com/v1/places:searchText"
            payload = {
                "textQuery": location,
                "maxResultCount": nb_results
            }
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": os.getenv('GOOGLE_API_KEY'),
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location"
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            location_data = response.json()
            print(f"Location search response: {json.dumps(location_data, indent=2)}")

            if not location_data.get('places'):
                return {"error": "No places found for this location"}
            
            latitude = location_data['places'][0]['location']['latitude']
            longitude = location_data['places'][0]['location']['longitude']
            print(f"Using coordinates: lat={latitude}, long={longitude}")

            # Search activities with valid place types
            url = "https://places.googleapis.com/v1/places:searchNearby"
            payload = {
                "includedTypes": [
                    "tourist_attraction",
                    "museum",
                    "art_gallery",
                    "park",
                    "amusement_park"
                ],
                "maxResultCount": nb_results,
                "locationRestriction": {
                    "circle": {
                        "center": {"latitude": latitude, "longitude": longitude},
                        "radius": 30000.0
                    }
                }
            }
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": os.getenv('GOOGLE_API_KEY'),
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.id,places.rating,places.types"
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code != 200:
                error_data = response.json().get('error', {})
                error_message = error_data.get('message', 'Unknown error')
                return {"error": f"Activity search failed: {error_message}"}
                
            activities_data = response.json()

            # Format activities with additional information
            formatted_activities = []
            if activities_data.get('places'):
                for place in activities_data['places']:
                    formatted_activities.append({
                        "name": place['displayName']['text'],
                        "address": place['formattedAddress'],
                        "maps_link": f"https://www.google.com/maps/place/?q=place_id:{place['id']}",
                        "rating": place.get('rating', 'Not rated'),
                        "types": place.get('types', [])
                    })

            return {
                "result": f"Found {len(formatted_activities)} activities near {location}",
                "activities": formatted_activities
            }

        except (ValueError, TypeError) as e:
            return {"error": f"Erreur de conversion des nombres: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    # Create an instance of the activityTool
    activity_tool = ActivityTool()

    # Define the parameters
    params = {
        "location": "Paris",
        "nb_results": 10
    }

    # Call the execute method with the parameters
    result = activity_tool.execute(**params)

    # Print the result
    print(result)