from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from typing import List, Dict, Any
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CarHireSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="car hire searcher",
            description="Search for car hire locations using Skyscanner API"
        )
        self.api_key = os.getenv('SKYSCANNER_API_KEY')
        self.base_url = "https://partners.api.skyscanner.net/apiservices/v3"

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="search_term",
                param_type=ParameterType.STRING,
                description="Location to search for car hire (e.g., 'Paris')",
                required=True
            ),
            ToolParameter(
                name="market",
                param_type=ParameterType.STRING,
                description="Market where search is coming from (e.g., 'UK')",
                required=False,
                default="UK"
            ),
            ToolParameter(
                name="locale",
                param_type=ParameterType.STRING,
                description="Language for the search (ISO locale)",
                required=False,
                default="en-GB"
            )
        ]

    def _get_location_suggestions(self, search_term: str, market: str, locale: str) -> Dict[str, Any]:
        url = f"{self.base_url}/autosuggest/carhire"
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": {
                "market": market,
                "locale": locale,
                "searchTerm": search_term
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            search_term = kwargs["search_term"]
            market = kwargs.get("market", "UK")
            locale = kwargs.get("locale", "en-GB")

            suggestions = self._get_location_suggestions(search_term, market, locale)
            
            # Format the response
            formatted_locations = []
            for place in suggestions.get('places', []):
                location_info = {
                    "name": place['name'],
                    "type": place['type'],
                    "coordinates": place.get('location', ''),
                    "hierarchy": place.get('hierarchy', ''),
                    "entity_id": place['entityId']
                }
                formatted_locations.append(location_info)

            return {
                "result": f"Found {len(formatted_locations)} car hire locations matching '{search_term}'",
                "market": market,
                "locale": locale,
                "locations": formatted_locations
            }

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    # Create an instance of the CarHireSearchTool
    car_tool = CarHireSearchTool()

    # Test parameters
    params = {
        "search_term": "London",
        "market": "UK",
        "locale": "en-GB"
    }

    # Call the execute method with the parameters
    result = car_tool.execute(**params)

    # Print the result
    print(json.dumps(result, indent=2))
