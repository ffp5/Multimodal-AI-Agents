from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from typing import List, Dict, Any
import requests
import time
from math import cos, radians
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

class HotelToolOpen(BaseTool):
    def __init__(self):
        super().__init__(
            name="hotel_searcher",
            description="Recherche d'hôtels sur OpenStreetMap et renvoie les n premiers résultats",
        )
        self.nominatim_endpoint = "https://nominatim.openstreetmap.org"

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="location",
                param_type=ParameterType.STRING,
                description="Localisation de l'hôtel, met le nom de la ville et le pays",
                required=True
            ),
            ToolParameter(
                name="nb_results",
                param_type=ParameterType.INTEGER,
                description="Nombre de résultats à renvoyer (par défaut 6)",
                required=False,
            )
        ]

    def _get_coordinates(self, location: str) -> tuple:
        """Obtenir les coordonnées d'une localisation via Nominatim."""
        headers = {
            'User-Agent': 'HotelSearchTool/1.0'
        }
        params = {
            'q': location,
            'format': 'json',
            'limit': 1
        }
        
        response = requests.get(
            f"{self.nominatim_endpoint}/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        data = response.json()
        if not data:
            raise ValueError(f"Aucun lieu trouvé pour: {location}")
            
        return float(data[0]['lat']), float(data[0]['lon'])

    def _search_hotels(self, latitude: float, longitude: float, nb_results: int) -> List[Dict]:
        """
        Rechercher les hôtels autour d'un point via Nominatim en utilisant une viewbox.
        La viewbox est calculée pour un rayon d'environ 30 km.
        """
        headers = {
            'User-Agent': 'HotelSearchTool/1.0'
        }
        # Calcul du décalage en degrés pour 30 km (approximativement)
        delta_lat = 30000 / 111000  # environ 0.27 degré
        delta_lon = 30000 / (111000 * cos(radians(latitude)))
        
        min_lat = latitude - delta_lat
        max_lat = latitude + delta_lat
        min_lon = longitude - delta_lon
        max_lon = longitude + delta_lon

        params = {
            'q': 'hotel',  # Rechercher le terme "hotel"
            'format': 'json',
            'limit': nb_results,
            # La viewbox se définit par: left, top, right, bottom
            'viewbox': f"{min_lon},{max_lat},{max_lon},{min_lat}",
            'bounded': 1,  # Restreint la recherche à la viewbox
        }
        
        response = requests.get(
            f"{self.nominatim_endpoint}/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            location = kwargs["location"]
            nb_results = int(kwargs.get("nb_results", 6))
            
            # Obtenir les coordonnées de la localisation
            latitude, longitude = self._get_coordinates(location)
            time.sleep(1)  # Respect de la politique d'utilisation de Nominatim
            
            # Rechercher les hôtels dans la zone délimitée
            hotels_data = self._search_hotels(latitude, longitude, nb_results)
            
            # Formater les résultats
            formatted_hotels = []
            for hotel in hotels_data:
                osm_id = hotel.get('osm_id', '')
                formatted_hotels.append({
                    "name": hotel.get('display_name', '').split(',')[0],  # On récupère la première partie comme nom
                    "address": hotel.get('display_name', ''),
                    "maps_link": f"https://www.openstreetmap.org/way/{osm_id}"
                })

            output = {
                "hotels": formatted_hotels
            }
            print(f"Réponse du tool: {output}")
            return output

        except ValueError as e:
            return {"error": f"Erreur: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Création d'une instance du HotelToolOpen
    hotel_tool = HotelToolOpen()

    # Définition des paramètres
    params = {
        "location": "Paris",
        "nb_results": 3
    }

    # Appel de la méthode execute avec les paramètres
    result = hotel_tool.execute(**params)
