import googlemaps
from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
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
                name="list of locations",
                param_type=ParameterType.LIST,
                description="List of locations to calculate distances from the origin",
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
        locations = kwargs.get("list_of_locations")  # Changed from "list of locations" to "list_of_locations"
        mode = kwargs.get("mode", "driving")
        api_key = kwargs.get("api_key")

        # Input validation
        if not locations or not api_key:
            return {"error": "Missing required parameters: list_of_locations and api_key are required."}

        # Ensure locations is a list with at least two elements
        if not isinstance(locations, list) or len(locations) < 2:
            return {"error": "list_of_locations must be a list with at least two locations"}

        dict_result = {}
        # Process locations as pairs
        for i in range(len(locations)-1):
            origin = locations[i]
            destination = locations[i+1]

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
                        }
                        dict_result[f"{origin} to {destination}"] = formatted_result
                    else:
                        dict_result[f"{origin} to {destination}"] = {
                            "error": f"Route calculation failed: {element['status']}"
                        }
                else:
                    return {"error": f"API request failed: {result['status']}"}

            except Exception as e:
                return {"error": f"An error occurred: {str(e)}"}
        
        return dict_result

# Example usage:
if __name__ == "__main__":
    tool = MapsTool()
    result = tool.execute(
        list_of_locations=["New York City", "Los Angeles", "Las Vegas"],  # Changed parameter name
        mode="driving",
        api_key="AIzaSyD6r9ETEBygVtqEEAlcXu7WLMj4fkbhnig"
    )
    print(result)

