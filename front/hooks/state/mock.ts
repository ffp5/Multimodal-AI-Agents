import type { Trip } from "./tripsStore";

export const mockTrips: Trip[] = [
	{
		id: "1",
		name: "Super Trip",
		input: {
			days: 10,
			start: "Paris, France",
			destination: "Loire, France",
		},
		output: {
			roadTrip: {
				titre: "Road Trip en France",
				dates: {
					debut: "2025-05-01",
					fin: "2025-05-10",
				},
				etapes: [
					{
						jour: 1,
						date: "2025-05-01",
						region: "Paris",
						activites: [
							{
								nom: "Visite de la Tour Eiffel",
								description:
									"Découverte de la Tour Eiffel et promenade dans le Champ-de-Mars",
								horaire: "09:00-12:00",
							},
							{
								nom: "Exploration du Musée du Louvre",
								description:
									"Visite guidée des chefs-d'œuvre du musée",
								horaire: "14:00-17:00",
							},
						],
					},
					{
						jour: 2,
						date: "2025-05-02",
						region: "Vallée de la Loire",
						activites: [
							{
								nom: "Visite du Château de Chambord",
								description:
									"Découverte du château emblématique de la Renaissance",
								horaire: "10:00-13:00",
							},
							{
								nom: "Dégustation de vins",
								description:
									"Dégustation dans un domaine viticole local",
								horaire: "15:00-17:00",
							},
						],
					},
				],
				locationVoiture: {
					compagnie: "Rent-A-Car France",
					lieuPriseEnCharge: "Aéroport Charles de Gaulle, Paris",
					dateHeurePrise: "2025-05-01T08:00:00",
					lieuRestitution: "Aéroport Charles de Gaulle, Paris",
					dateHeureRestitution: "2025-05-10T18:00:00",
					typeVehicule: "SUV",
					tarifJournalier: 75.5,
					devise: "EUR",
				},
			},
		},
		loading: false,
	},
];
