"use client";

import { create } from "zustand";
import { z } from "zod";
import { createSelectors } from "./selectors";
import { get } from "react-hook-form";
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

// Define types for the server output structure

export interface Activity {
	nom: string;
	description: string;
	horaire: string;
}

export interface Etape {
	jour: number;
	date: string;
	region: string;
	activites: Activity[];
}

export interface LocationVoiture {
	compagnie: string;
	lieuPriseEnCharge: string;
	dateHeurePrise: string;
	lieuRestitution: string;
	dateHeureRestitution: string;
	typeVehicule: string;
	tarifJournalier: number;
	devise: string;
}

export interface RoadTrip {
	titre: string;
	dates: {
		debut: string;
		fin: string;
	};
	etapes: Etape[];
	locationVoiture: LocationVoiture;
}

export type TripOutput = {
	roadTrip: RoadTrip;
};

// Define the Trip type for storing each trip in the store
export interface Trip {
	id: string;
	name: string;
	input: TripInput;
	output?: TripOutput;
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
