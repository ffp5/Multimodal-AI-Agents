system_prompt = """Tu es un assistant capable d'utiliser des outils pour accomplir des tâches.
            Utilise les outils à ta disposition autant que nécessaire pour accomplir la tâche demandée.
            Entre chaque étape, tu dois m'expliquer tres brievement ce que tu vas faire.
            IMPORTANT : Apres avoir fini tes tâches, tu dois terminer la conversation en utilisant l'outil 'stop'.
            """

system_prompt_road_trip_planner = """Tu es un assistant capable d'utiliser des outils pour accomplir des tâches.
            Utilise les outils à ta disposition autant que nécessaire pour accomplir la tâche demandée.
            Entre chaque étape, tu dois m'expliquer tres brievement ton raisonnement et ce que tu vas faire.
            IMPORTANT : Apres avoir fini tes tâches, tu dois terminer la conversation en utilisant l'outil 'stop'.
            """

json_output = {
    "road_trip_planner": {
        "input": {
            "start": "Paris",
            "end": "Marseille",
            "waypoints": ["Lyon", "Nice"],
            "travel_mode": "driving",
            "departure_time": "2021-06-01T12:00:00",
            "arrival_time": "2021-06-01T20:00:00"
        },
        "output": {
            "route": {
                "start": "Paris",
                "end": "Marseille",
                "waypoints": ["Lyon", "Nice"],
                "departure_time": "2021-06-01T12:00:00",
                "arrival_time": "2021-06-01T20:00:00",
                "distance": 775.4,
                "duration": 7.5,
                "steps": [
                    {
                        "start": "Paris",
                        "end": "Lyon",
                        "distance": 466.3,
                        "duration": 4.5
                    },
                    {
                        "start": "Lyon",
                        "end": "Nice",
                        "distance": 219.1,
                        "duration": 3
                    },
                    {
                        "start": "Nice",
                        "end": "Marseille",
                        "distance": 90,
                        "duration": 1
                    }
                ]
            },
            "hotels": [
                {
                    "city": "Lyon",
                    "name": "Hotel Lyon Center",
                    "rating": 4.5,
                    "price": 120,
                    "address": "123 Lyon Street"
                },
                {
                    "city": "Nice",
                    "name": "Nice Beach Hotel",
                    "rating": 4.2,
                    "price": 150,
                    "address": "456 Nice Avenue"
                }
            ],
            "car_rentals": [
                {
                    "city": "Paris",
                    "company": "EuroCar",
                    "vehicle_type": "Sedan",
                    "price_per_day": 50,
                    "pickup_location": "Paris Central Station"
                },
                {
                    "city": "Marseille",
                    "company": "AutoFrance",
                    "vehicle_type": "SUV",
                    "price_per_day": 65,
                    "pickup_location": "Marseille Airport"
                }
            ]
        }
    }
}