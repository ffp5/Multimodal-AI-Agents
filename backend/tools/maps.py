import googlemaps
from tools.base_tool import BaseTool, ToolParameter, ParameterType
from typing import List, Dict, Any

class MapsTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="maps api",
            description="Tool that returns distances and travel durations between origins and destinations using the Google Maps API."
        )

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="origin",
                param_type=ParameterType.STRING,
                description="Origin location (address or place name)",
                required=True
            ),
            ToolParameter(
                name="destination",
                param_type=ParameterType.STRING,
                description="Destination location (address or place name)",
                required=True
            ),
            ToolParameter(
                name="mode",
                param_type=ParameterType.STRING,
                description="Travel mode (e.g., 'driving', 'walking', 'transit', 'bicycling')",
                required=False,
                default="driving"
            ),
            ToolParameter(
                name="api_key",
                param_type=ParameterType.STRING,
                description="Google Maps API key",
                required=True
            )
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        origin = kwargs.get("origin")
        destination = kwargs.get("destination")
        mode = kwargs.get("mode", "driving")
        api_key = kwargs.get("api_key")

        if not origin or not destination or not api_key:
            return {"error": "Missing required parameters: origin, destination, and api_key are required."}

        try:
            # Initialize the Google Maps client
            gmaps = googlemaps.Client(key=api_key)
            
            # Get the distance matrix
            result = gmaps.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode=mode
            )

            if result['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    formatted_result = {
                        'origin': result['origin_addresses'][0],
                        'destination': result['destination_addresses'][0],
                        'distance': element['distance']['text'],
                        'duration': element['duration']['text'],
                        'distance_meters': element['distance']['value'],
                        'duration_seconds': element['duration']['value']
                    }
                    return {"result": formatted_result}
                else:
                    return {"error": f"Route calculation failed: {element['status']}"}
            else:
                return {"error": f"API request failed: {result['status']}"}

        except Exception as e:
            return {"error": str(e)}

# Example usage:
if __name__ == "__main__":
    tool = MapsTool()
    result = tool.execute(
        origin="New York City",
        destination="Los Angeles",
        mode="driving",
        api_key="AIzaSyD6r9ETEBygVtqEEAlcXu7WLMj4fkbhnig"
    )
    print(result)

