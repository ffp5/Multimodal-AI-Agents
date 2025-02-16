"use client";

import { create } from "zustand";
import { z } from "zod";
import { createSelectors } from "./selectors";
import { mockTrips } from "./mock";

// Define the form inputs schema using zod
export const formSchema = z.object({
	start: z.string().min(2, {
		message: "Please enter a valid starting location.",
	}),
	destination: z.string().min(2, {
		message: "Please enter a valid destination.",
	}),
	days: z
		.number({ invalid_type_error: "Number of days is required" })
		.min(1, {
			message: "There must be at least 1 day for the trip.",
		}),
});

export type TripInput = z.infer<typeof formSchema>;

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

// Define the Trip type for storing each trip in the store
export interface Trip {
	id: string;
	name: string;
	input: TripInput;
	output?: z.infer<typeof TripOutputSchema>;
	loading: boolean;
	error?: string;
}

// Define the interface for the trip store
interface TripStore {
	trips: Trip[];
	currentTripId: string | null;
}

// Create the Zustand store
export const useTripStoreBase = create<TripStore>((set, get) => ({
	trips: mockTrips,
	currentTripId: null,
}));

export const useTripStore = createSelectors(useTripStoreBase);
