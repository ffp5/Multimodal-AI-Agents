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

class HotelTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="hotel_searcher",
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
            #print(f"Location search response: {json.dumps(location_data, indent=2)}")

            if not location_data.get('places'):
                return {"error": "No places found for this location"}
            
            latitude = location_data['places'][0]['location']['latitude']
            longitude = location_data['places'][0]['location']['longitude']
            #print(f"Using coordinates: lat={latitude}, long={longitude}")

            # Search hotels
            url = "https://places.googleapis.com/v1/places:searchNearby"
            payload = {
                "includedTypes": ['hotel', 'lodging', 'bed_and_breakfast', 'motel', 'farmstay', "guest_house"],
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
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.id"
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code != 200:
                return {"error": f"Hotel search failed: {response.text}"}
                
            hotels_data = response.json()
            #print(f"Hotels search response: {json.dumps(hotels_data, indent=2)}")

            # Format hotels inline: output name, address, and Google Maps link
            formatted_hotels = []
            if hotels_data.get('places'):
                for place in hotels_data['places']:
                    maps_link = f"https://www.google.com/maps/place/?q=place_id:{place['id']}"
                    formatted_hotels.append({
                        "name": place['displayName']['text'],
                        "address": place['formattedAddress'],
                        "maps_link": maps_link
                    })
            output= {
                "hotels": formatted_hotels
            }
            print(f"Réaponse du tool: {output}")
            return output

        except (ValueError, TypeError) as e:
            return {"error": f"Erreur de conversion des nombres: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Create an instance of the HotelTool
    hotel_tool = HotelTool()

    # Define the parameters
    params = {
        "location": "Paris",
        "nb_results": 10
    }

    # Call the execute method with the parameters
    result = hotel_tool.execute(**params)

    # #print the result
    #print(result)