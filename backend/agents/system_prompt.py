system_prompt = """Tu es un assistant capable d'utiliser des outils pour accomplir des tâches.
            Utilise les outils à ta disposition autant que nécessaire pour accomplir la tâche demandée.
            Entre chaque étape, tu dois m'expliquer tres brievement ce que tu vas faire.
            IMPORTANT : Apres avoir fini tes tâches, tu dois terminer la conversation en utilisant l'outil 'stop'.
            """

system_prompt_road_trip_planner = """Tu es un assistant capable d'utiliser des outils pour accomplir des tâches.
            Utilise les outils à ta disposition autant que nécessaire pour accomplir la tâche demandée.
            Avant chaque étape, tu dois m'expliquer tres brievement (4 mots MAXIMUM) ton raisonnement et ce que tu vas faire.
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


proposed_dict_output = {
  "tripTitle": "Road Trip in France",
  "version": "1.0",
  "tripOverview": {
    "description": "An exciting road trip across France visiting iconic landmarks, museums, castles, and vineyards while enjoying comfortable travel.",
    "totalDays": 2,
    "primaryLanguage": "English",
    "currency": "$"
  },
  "days": [
    {
      "dayNumber": 1,
      "location": "Paris, France",
      "description": "Paris is the vibrant capital of France, known for its historical monuments, world-class art museums, gourmet restaurants, and cultural festivals. Start your day with a visit to the Eiffel Tower to enjoy panoramic views, then continue to the Louvre Museum to admire timeless masterpieces.",
      "activities": [
        {
          "type": "sightseeing",
          "name": "Eiffel Tower Visit",
          "description": "Explore and enjoy panoramic views from the Eiffel Tower and walk around Champ-de-Mars.",
          "schedule": {
            "start": "09:00",
            "end": "12:00"
          }
        },
        {
          "type": "museum-visits",
          "name": "Louvre Museum Guided Tour",
          "description": "Guided tour through the Louvre to see the key art works and exhibits.",
          "schedule": {
            "start": "14:00",
            "end": "17:00"
          }
        },
        {
          "type": "transport",
          "mode": "car",
          "durationSeconds": 7200,
          "description": "Local car transportation between different attractions."
        }
      ]
    },
    {
      "dayNumber": 2,
      "location": "Loire Valley, France",
      "description": "The Loire Valley is famed for its majestic châteaux, scenic landscapes, and renowned vineyards. Begin your day with a visit to the iconic Château de Chambord from the Renaissance era and later enjoy a local wine tasting at a vineyard near Château de Chenonceau.",
      "activities": [
        {
          "type": "sightseeing",
          "name": "Château de Chambord Visit",
          "description": "Discover the magnificence of the Renaissance-era castle.",
          "schedule": {
            "start": "10:00",
            "end": "13:00"
          }
        },
        {
          "type": "culinary",
          "name": "Vineyard Wine Tasting",
          "description": "Experience local wines and learn about the winemaking process at a nearby vineyard.",
          "schedule": {
            "start": "15:00",
            "end": "17:00"
          }
        }
      ]
    }
  ],
  "carRental": {
    "company": "Rent-A-Car France",
    "pickupLocation": "Charles de Gaulle Airport, Paris",
    "pickupDateTime": "2025-05-01T08:00:00",
    "returnLocation": "Charles de Gaulle Airport, Paris",
    "returnDateTime": "2025-05-10T18:00:00",
    "vehicleType": "SUV",
    "dailyRate": 75.50,
    "currency": "EUR",
    "extras": {
      "insuranceIncluded": True,
      "mileageLimit": "Unlimited",
      "notes": "Ensure to check fuel policy and local driving rules."
    }
  },
  "metadata": {
    "createdDate": "2025-02-16T07:15:49Z",
    "lastUpdated": "2025-04-01T12:00:00Z",
    "version": "1.0"
  }
}

return_instructions = """
// Common schedule schema for activities that include time information.
const ScheduleSchema = z.object({
	start: z.string(), // e.g., "09:00"
	end: z.string(), // e.g., "12:00"
});

// Define an enum for the 20 possible road trip activity types.
const OtherActivityType = z.enum([
	"sightseeing",
	"culinary",
	"adventure",
	"hiking",
	"camping",
	"museum",
	"landmark",
	"shopping",
	"local-market",
	"cultural-tour",
	"wildlife",
	"beach",
	"scenic-drive",
	"historical-exploration",
	"photo-op",
	"wine-tasting",
	"gastronomic",
	"local-festival",
	"relaxation",
	"sporting-activities",
]);

// Activity schema for non-car activities.
const OtherActivitySchema = z.object({
	type: OtherActivityType, // type is one of the 20 enum values above.
	name: z.string(),
	description: z.string(),
	schedule: ScheduleSchema,
});

// Activity schema for car activities.
const CarActivitySchema = z.object({
	type: z.literal("car"),
	description: z.string(),
	mode: z.string(), // Example: "rental", "local transport", etc.
	durationSeconds: z.number(),
});

// Union of both activity types.
const ActivitySchema = z.union([CarActivitySchema, OtherActivitySchema]);

// Hotel schema added to each day.
const HotelSchema = z.object({
	name: z.string(),
	address: z.string(),
	stars: z.number(), // Star rating (e.g., 3, 4, 5)
	image: z.string().optional(), // Optional image URL
});

// Day schema now includes a hotel key and an optional notes field.
const DaySchema = z.object({
	dayNumber: z.number(),
	location: z.string(),
	description: z.string(),
	activities: z.array(ActivitySchema),
	hotel: HotelSchema,
	notes: z.string().optional(), // Optional notes for the day
});

// Car rental extras schema.
const CarRentalExtrasSchema = z.object({
	insuranceIncluded: z.boolean(),
	mileageLimit: z.string(),
	notes: z.string(),
});

// Car rental details schema.
const CarRentalSchema = z.object({
	company: z.string(),
	pickupLocation: z.string(),
	pickupDateTime: z.string(),
	returnLocation: z.string(),
	returnDateTime: z.string(),
	vehicleType: z.string(),
	dailyRate: z.number(),
	currency: z.string(),
	extras: CarRentalExtrasSchema,
});

// Metadata schema.
const MetadataSchema = z.object({
	createdDate: z.string(),
	lastUpdated: z.string(),
	version: z.string(),
});

// Trip overview schema.
const TripOverviewSchema = z.object({
	description: z.string(),
	totalDays: z.number(),
	primaryLanguage: z.string(),
	currency: z.string(),
});

// Main Trip schema.
export const TripOutputSchema = z.object({
	tripTitle: z.string(),
	version: z.string(),
	tripOverview: TripOverviewSchema,
	days: z.array(DaySchema),
	carRental: CarRentalSchema,
	metadata: MetadataSchema,
});
"""