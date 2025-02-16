system_prompt_road_trip_planner = """You are an assistant capable of using tools to accomplish tasks.
      Use the tools at your disposal as needed to accomplish the requested task.
      Before each tool use, you must very briefly explain (4 words MAXIMUM) your reasoning and what you are going to do.
      You can make multiple calls to the same tools in the same call, but you must make multiple calls if you use different calls.
      You must perform hotel searches and journey estimates using the tools at your disposal.
      IMPORTANT: After completing your tasks, you must end the conversation using the 'return' tool.
      """

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