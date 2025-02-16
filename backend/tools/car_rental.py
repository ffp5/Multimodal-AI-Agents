from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from typing import List, Dict, Any
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CarRentalTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="car rental searcher",
            description="Search for car rental locations in a specified area"
        )

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="location",
                param_type=ParameterType.STRING,
                description="Location to search for car rentals",
                required=True
            ),
            ToolParameter(
                name="nb_results",
                param_type=ParameterType.INTEGER,
                description="Number of results to return",
                required=False,
                default=5
            )
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            location = kwargs["location"]
            nb_results = int(kwargs.get("nb_results", 5))
            
            # Get location coordinates
            url = "https://places.googleapis.com/v1/places:searchText"
            payload = {
                "textQuery": location,
                "maxResultCount": 1
            }
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": os.getenv('GOOGLE_API_KEY'),
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location"
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            location_data = response.json()

            if not location_data.get('places'):
                return {"error": "No location found"}
            
            latitude = location_data['places'][0]['location']['latitude']
            longitude = location_data['places'][0]['location']['longitude']

            # Search for car rental locations
            url = "https://places.googleapis.com/v1/places:searchNearby"
            payload = {
                "includedTypes": ["car_rental"],
                "maxResultCount": nb_results,
                "locationRestriction": {
                    "circle": {
                        "center": {"latitude": latitude, "longitude": longitude},
                        "radius": 50000.0  # 50km radius
                    }
                }
            }
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": os.getenv('GOOGLE_API_KEY'),
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.id,places.rating,places.phoneNumber,places.websiteUri,places.currentOpeningHours"
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code != 200:
                error_data = response.json().get('error', {})
                error_message = error_data.get('message', 'Unknown error')
                return {"error": f"Car rental search failed: {error_message}"}
            
            rental_data = response.json()
            
            # Format rental locations with additional information
            formatted_rentals = []
            if rental_data.get('places'):
                for place in rental_data['places']:
                    rental_info = {
                        "name": place['displayName']['text'],
                        "address": place['formattedAddress'],
                        "maps_link": f"https://www.google.com/maps/place/?q=place_id:{place['id']}",
                        "rating": place.get('rating', 'Not rated'),
                        "phone": place.get('phoneNumber', 'No phone number available'),
                        "website": place.get('websiteUri', 'No website available')
                    }
                    
                    # Add opening hours if available
                    if 'currentOpeningHours' in place:
                        rental_info['hours'] = place['currentOpeningHours'].get('weekdayDescriptions', [])
                    
                    formatted_rentals.append(rental_info)

            return {
                "result": f"Found {len(formatted_rentals)} car rental locations near {location}",
                "rentals": formatted_rentals
            }

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    # Create an instance of the CarRentalTool
    rental_tool = CarRentalTool()

    # Define the parameters
    params = {
        "location": "Paris",
        "nb_results": 5
    }

    # Call the execute method with the parameters
    result = rental_tool.execute(**params)

    # Print the result
    print(json.dumps(result, indent=2))
