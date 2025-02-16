from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from backend.agents.system_prompt import return_instructions
from backend.utils.convert_osm_to_maps import convert_osm_to_maps
import json


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
                description="Retourne les infromations sous ce format JSON en respectant ce format:\n\n" + return_instructions,
                required=True,
            )
        ]

    def execute(self, result: str) -> dict:
        # On convertit la réponse du llm en json
        #[function]: {"result": {"roadTrip": {"titre": "Road Trip en France", "dates": {"debut": "2025-05-01", "fin": "2025-05-05"}, "etapes": [{"jour": 1, "date": "2025-05-01", "region": "Paris", "activites": [{"nom": "Visite de la Tour Eiffel", "description": "D\u00e9couverte de la Tour Eiffel et promenade dans le Champ-de-Mars", "horaire": "09:00-12:00"}, {"nom": "Exploration du Mus\u00e9e du Louvre", "description": "Visite guid\u00e9e des chefs-d'\u0153uvre du mus\u00e9e", "horaire": "14:00-17:00"}], "hotel": {"nom": "The Atrium Hotel & Conference Centre", "adresse": "Avenue du Bois de la Pie, Roissy-en-France, Sarcelles, Val-d'Oise, France m\u00e9tropolitaine, 95700, France", "lienCarte": "https://www.openstreetmap.org/way/104936811"}}, {"jour": 2, "date": "2025-05-02", "region": "Lyon", "activites": [{"nom": "Visite de la Basilique Notre-Dame de Fourvi\u00e8re", "description": "D\u00e9couverte de la basilique et panorama sur la ville", "horaire": "10:00-12:00"}, {"nom": "Balade dans le Vieux Lyon", "description": "Exploration des ruelles m\u00e9di\u00e9vales du quartier historique", "horaire": "14:00-16:00"}], "hotel": {"nom": "B&B Hotel Massieux Genay", "adresse": "662B, Rue des Jonch\u00e8res, Champ Fleuri, Genay, Lyon, M\u00e9tropole de Lyon, Rh\u00f4ne, Auvergne-Rh\u00f4ne-Alpes, France m\u00e9tropolitaine, 69730, France", "lienCarte": "https://www.openstreetmap.org/way/12472748567"}}, {"jour": 3, "date": "2025-05-03", "region": "Lyon", "activites": [{"nom": "Visite du Parc de la T\u00eate d'Or", "description": "D\u00e9tente et d\u00e9couverte du parc zoologique", "horaire": "09:00-12:00"}], "hotel": {"nom": "Slo Living Hostel", "adresse": "Rue Bonnefoi, Voltaire, Lyon 3e Arrondissement, Lyon, M\u00e9tropole de Lyon, Rh\u00f4ne, Auvergne-Rh\u00f4ne-Alpes, France m\u00e9tropolitaine, 69003, France", "lienCarte": "https://www.openstreetmap.org/way/3305697821"}}, {"jour": 4, "date": "2025-05-04", "region": "Marseille", "activites": [{"nom": "Visite du Vieux-Port", "description": "D\u00e9couverte du port historique et ambiance m\u00e9diterran\u00e9enne", "horaire": "10:00-12:00"}, {"nom": "Visite de la Basilique Notre-Dame de la Garde", "description": "D\u00e9couverte de la basilique et vue panoramique sur Marseille", "horaire": "14:00-16:00"}], "hotel": {"nom": "B&B Hotel", "adresse": "8, Avenue Elsa Triolet, La Vieille-Chapelle, Marseille 8e Arrondissement, Marseille, Bouches-du-Rh\u00f4ne, Provence-Alpes-C\u00f4te d'Azur, France m\u00e9tropolitaine, 13008, France", "lienCarte": "https://www.openstreetmap.org/way/793080141"}}, {"jour": 5, "date": "2025-05-05", "region": "Marseille", "activites": [{"nom": "Balade dans le quartier du Panier", "description": "Exploration du plus vieux quartier de Marseille", "horaire": "09:00-11:00"}], "hotel": {"nom": "H\u00f4tel Europe", "adresse": "Rue Beauvau, Op\u00e9ra, Marseille 1er Arrondissement, Marseille, Bouches-du-Rh\u00f4ne, Provence-Alpes-C\u00f4te d'Azur, France m\u00e9tropolitaine, 13001, France", "lienCarte": "https://www.openstreetmap.org/way/1941641133"}}], "locationVoiture": {"compagnie": "Rent-A-Car France", "lieuPriseEnCharge": "A\u00e9roport Charles de Gaulle, Paris", "dateHeurePrise": "2025-05-01T08:00:00", "lieuRestitution": "A\u00e9roport Charles de Gaulle, Paris", "dateHeureRestitution": "2025-05-05T18:00:00", "typeVehicule": "SUV", "tarifJournalier": 75.5, "devise": "EUR"}}}}
        try:
            result_json = json.loads(result)
            # On convertit tous les liens openstreetmap en lien google maps
            try:
                for etape in result_json["roadTrip"]["etapes"]:
                    etape["hotel"]["lienCarte"] = convert_osm_to_maps(etape["hotel"]["lienCarte"])
            except:
                pass
        
        except Exception as e:
            raise ValueError(f"Erreur lors de la conversion de la réponse en JSON : {e}")

        return {
            "result": result_json,
        }
