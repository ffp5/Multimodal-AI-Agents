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
			tripTitle: "Road Trip in France",
			version: "1.0",
			tripOverview: {
				description:
					"Explore the beauty of France, from iconic landmarks to charming villages.",
				totalDays: 2,
				primaryLanguage: "English",
				currency: "$",
			},
			days: [
				{
					dayNumber: 1,
					location: "Paris, France",
					description:
						"Start your journey in the heart of Paris, exploring timeless landmarks and local culture.",
					activities: [
						{
							type: "sightseeing",
							name: "Eiffel Tower Visit",
							description:
								"Enjoy panoramic views from the Eiffel Tower.",
							schedule: {
								start: "09:00",
								end: "11:00",
							},
						},
						{
							type: "car",
							description:
								"Drive between attractions within the city.",
							mode: "rental",
							durationSeconds: 3600,
						},
					],
					hotel: {
						name: "Parisian Elegance Hotel",
						address: "123 Champs-Élysées, Paris, France",
						stars: 5,
						image: "https://example.com/hotel-paris.jpg",
					},
					notes: "Be prepared for busy streets and vibrant local life.",
				},
				{
					dayNumber: 2,
					location: "Loire Valley, France",
					description:
						"Discover the historic châteaux and serene landscapes of the Loire Valley.",
					activities: [
						{
							type: "historical-exploration",
							name: "Visit Château de Chambord",
							description:
								"Explore the magnificent Renaissance-era castle.",
							schedule: {
								start: "10:00",
								end: "13:00",
							},
						},
						{
							type: "wine-tasting",
							name: "Local Vineyard Experience",
							description:
								"Taste exquisite wines and learn about the winemaking process.",
							schedule: {
								start: "15:00",
								end: "17:00",
							},
						},
					],
					hotel: {
						name: "Loire Valley Inn",
						address: "456 River Road, Amboise, France",
						stars: 4,
						image: "https://example.com/hotel-loire.jpg",
					},
					notes: "Don't miss the picturesque sunsets by the river.",
				},
			],
			carRental: {
				company: "Rent-A-Car France",
				pickupLocation: "Charles de Gaulle Airport, Paris",
				pickupDateTime: "2025-05-01T08:00:00",
				returnLocation: "Charles de Gaulle Airport, Paris",
				returnDateTime: "2025-05-10T18:00:00",
				vehicleType: "SUV",
				dailyRate: 75.5,
				currency: "EUR",
				extras: {
					insuranceIncluded: true,
					mileageLimit: "Unlimited",
					notes: "Check fuel policy and local driving regulations.",
				},
			},
			metadata: {
				createdDate: "2025-02-16T07:15:49Z",
				lastUpdated: "2025-04-01T12:00:00Z",
				version: "1.0",
			},
		},
		loading: false,
	},
];
