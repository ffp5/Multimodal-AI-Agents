import requests
from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from typing import List, Dict, Any
import time
from math import radians, sin, cos, sqrt, atan2

class OpenStreetMapTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="osm_api",
            description="Tool that returns distances and travel durations between origins and destinations using OpenStreetMap."
        )
        self.nominatim_endpoint = "https://nominatim.openstreetmap.org/search"
        self.osrm_endpoint = "https://router.project-osrm.org/route/v1"

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="list_of_locations",
                param_type=ParameterType.LIST,
                description="List of locations to calculate distances from the origin",
                required=True
            ),
            ToolParameter(
                name="mode",
                param_type=ParameterType.STRING,
                description="Travel mode (e.g., 'driving', 'walking', 'cycling')",
                required=False,
                default="driving"
            )
        ]

    def _get_coordinates(self, location: str) -> tuple:
        """Get coordinates for a location using Nominatim."""
        params = {
            'q': location,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'OpenStreetMapTool/1.0'
        }
        
        response = requests.get(self.nominatim_endpoint, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            raise ValueError(f"Location not found: {location}")
            
        return float(data[0]['lon']), float(data[0]['lat'])

    def _get_route(self, origin: tuple, destination: tuple, mode: str) -> Dict:
        """Get route information using OSRM."""
        # Convert mode to OSRM profile
        profile = {
            'driving': 'car',
            'walking': 'foot',
            'cycling': 'bike'
        }.get(mode, 'car')

        # Format coordinates for OSRM
        coords = f"{origin[0]},{origin[1]};{destination[0]},{destination[1]}"
        url = f"{self.osrm_endpoint}/{profile}/{coords}"
        
        params = {
            'overview': 'false'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()

    def _format_distance(self, meters: float) -> str:
        """Format distance in a human-readable format."""
        if meters >= 1000:
            return f"{meters/1000:.1f} km"
        return f"{meters:.0f} m"

    def _format_duration(self, seconds: float) -> str:
        """Format duration in a human-readable format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0:
            return f"{int(hours)} hours {int(minutes)} mins"
        return f"{int(minutes)} mins"

    def execute(self, **kwargs) -> Dict[str, Any]:
        locations = kwargs.get("list_of_locations")
        mode = kwargs.get("mode", "driving")

        # Input validation
        if not locations:
            return {"error": "Missing required parameter: list_of_locations"}
        if not isinstance(locations, list) or len(locations) < 2:
            return {"error": "list_of_locations must be a list with at least two locations"}

        dict_result = {}
        
        # Process locations as pairs
        for i in range(len(locations)-1):
            origin = locations[i]
            destination = locations[i+1]

            try:
                # Get coordinates for both locations
                origin_coords = self._get_coordinates(origin)
                time.sleep(1)  # Respect Nominatim's usage policy
                dest_coords = self._get_coordinates(destination)
                
                # Get route information
                route_data = self._get_route(origin_coords, dest_coords, mode)
                
                if route_data.get('code') == 'Ok':
                    route = route_data['routes'][0]
                    formatted_result = {
                        'origin': origin,
                        'destination': destination,
                        'distance': self._format_distance(route['distance']),
                        'duration': self._format_duration(route['duration'])
                    }
                    dict_result[f"{origin} to {destination}"] = formatted_result
                else:
                    dict_result[f"{origin} to {destination}"] = {
                        "error": "Route calculation failed"
                    }

            except Exception as e:
                dict_result[f"{origin} to {destination}"] = {
                    "error": f"An error occurred: {str(e)}"
                }
            
            time.sleep(1)  # Respect API rate limits
        
        return dict_result

# Example usage:
if __name__ == "__main__":
    tool = OpenStreetMapTool()
    result = tool.execute(
        list_of_locations=["New York City", "Los Angeles", "Las Vegas"],
        mode="driving"
    )
    print(result)