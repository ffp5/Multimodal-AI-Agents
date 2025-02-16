system_prompt = """Tu es un assistant capable d'utiliser des outils pour accomplir des tâches.
            Utilise les outils à ta disposition autant que nécessaire pour accomplir la tâche demandée.
            Entre chaque étape, tu dois m'expliquer tres brievement ce que tu vas faire.
            IMPORTANT : Apres avoir fini tes tâches, tu dois terminer la conversation en utilisant l'outil 'stop'.
            """

system_prompt_road_trip_planner = """Tu es un assistant capable d'utiliser des outils pour accomplir des tâches.
            Utilise les outils à ta disposition autant que nécessaire pour accomplir la tâche demandée.
            Avant chaque étape, tu dois m'expliquer tres brievement ton raisonnement et ce que tu vas faire.
            Il faut que tu fasses obligatoirement des recherces d'hotels et des estimation de trajet, en utilisant les outils a ta disposition. 
            IMPORTANT : Apres avoir fini tes tâches, tu dois terminer la conversation en utilisant l'outil 'return'.
            """

#JSON ouput, day by day, with for each day a list a spot to visit, each meetrics deplacement, and hotel and car rental
dict_output = {
  "roadTrip": {
    "titre": "Road Trip en France",
    "dates": {
      "debut": "2025-05-01",
      "fin": "2025-05-10"
    },
    "etapes": [
      {
        "jour": 1,
        "date": "2025-05-01",
        "region": "Paris",
        "activites": [
          {
            "nom": "Visite de la Tour Eiffel",
            "description": "Découverte de la Tour Eiffel et promenade dans le Champ-de-Mars",
            "horaire": "09:00-12:00"
          },
          {
            "nom": "Exploration du Musée du Louvre",
            "description": "Visite guidée des chefs-d'œuvre du musée",
            "horaire": "14:00-17:00"
          }
        ]
      },
      {
        "jour": 2,
        "date": "2025-05-02",
        "region": "Vallée de la Loire",
        "activites": [
          {
            "nom": "Visite du Château de Chambord",
            "description": "Découverte du château emblématique de la Renaissance",
            "horaire": "10:00-13:00"
          },
          {
            "nom": "Dégustation de vins",
            "description": "Dégustation dans un domaine viticole local",
            "horaire": "15:00-17:00"
          }
        ]
      }
    ],

    "locationVoiture": {
      "compagnie": "Rent-A-Car France",
      "lieuPriseEnCharge": "Aéroport Charles de Gaulle, Paris",
      "dateHeurePrise": "2025-05-01T08:00:00",
      "lieuRestitution": "Aéroport Charles de Gaulle, Paris",
      "dateHeureRestitution": "2025-05-10T18:00:00",
      "typeVehicule": "SUV",
      "tarifJournalier": 75.50,
      "devise": "EUR"
    }
  }
}
