"use client";

import React, { useMemo, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import type { z } from "zod";
import { useMutation } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import {
	Form,
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { AutocompleteComponent } from "@/components/ui/address-autocomplete/AutocompleteComponent";
import {
	formSchema,
	TripOutputSchema,
	useTripStore,
} from "@/hooks/state/tripsStore";
import { isNewTrip } from "@/lib/isNewTrip";
import { TripReportDialog } from "../trip-report/TripReportDialog";

// Derive our form values type from the zod schema.
type TripValues = z.infer<typeof formSchema>;
// Define a discriminated union type for a chunk:
type Chunk = MessageChunk | ToolCallChunk | ToolResultChunk | ErrorChunk;

interface MessageChunk {
	type: "message";
	data: {
		role: "system" | "assistant" | "user";
		content: string;
		name: string | null;
		tool_call_id: string | null;
	};
}

interface ToolCallChunk {
	type: "tool_call";
	data: {
		tool_name: string;
		parameters: Record<string, any>;
	};
}

interface ToolResultChunk {
	type: "tool_result";
	data: {
		tool_name: string;
		result: any;
	};
}

interface ErrorChunk {
	type: "error";
	data: {
		message: string;
	};
}

export function TripForm() {
	const trips = useTripStore((state) => state.trips);
	const currentTripId = useTripStore((state) => state.currentTripId);
	const currentTrip = useMemo(() => {
		return trips.find((trip) => trip.id === currentTripId);
	}, [trips, currentTripId]);

	// Local state for assistant status.
	const [assistantStatus, setAssistantStatus] = useState("");

	// 1. Define your form.
	const form = useForm<TripValues>({
		resolver: zodResolver(formSchema),
		values: {
			start: currentTrip?.input.start || "",
			destination: currentTrip?.input.destination || "",
			days: currentTrip?.input.days || 1,
		},
	});

	const newTrip = isNewTrip(currentTrip, form.getValues());

	// 2. Streaming request function.
	async function streamTripRequest(data: TripValues) {
		const response = await fetch(
			"http://10.20.7.222:5000/plan-trip-stream",
			{
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					duration: data.days,
					end_location: data.destination,
					start_location: data.start,
				}),
			},
		);

		if (!response.ok || !response.body) {
			throw new Error("Network error");
		}

		const reader = response.body.getReader();
		const decoder = new TextDecoder();

		// Clear any existing assistant status.
		setAssistantStatus("");

		let finalChunk: Chunk | null = null;

		// Read stream chunks.
		while (true) {
			const { done, value } = await reader.read();
			if (done) break;
			const chunkString = decoder.decode(value, { stream: true });
			// Handle cases where multiple data lines may be present in one chunk.
			const lines = chunkString.split("\n");
			for (const line of lines) {
				if (line.startsWith("data: ")) {
					try {
						const parsedData = JSON.parse(
							line.slice("data: ".length),
						);
						const chunk: Chunk = parsedData;
						finalChunk = chunk;

						// Update assistant status if the chunk is an assistant message.
						if (
							chunk.type === "message" &&
							chunk.data.role === "assistant"
						) {
							setAssistantStatus(chunk.data.content);
						}
					} catch (error) {
						console.error("Error parsing stream chunk:", error);
					}
				}
			}
		}

		// Clear assistant status once the streaming is done.
		setAssistantStatus("");

		if (!finalChunk) {
			throw new Error("No data received from stream");
		}

		const finalData = finalChunk.data;
		console.log(finalData);

		const result = await TripOutputSchema.parseAsync(finalData);
		return result;
	}

	// 3. Use Tanstack Query mutation.
	const mutation = useMutation<
		z.infer<typeof TripOutputSchema>,
		Error,
		TripValues
	>({
		mutationFn: streamTripRequest,
		onMutate: () => {
			// Clear assistant status when starting a new request.
			setAssistantStatus("");
		},
		onSuccess: (data) => {
			const tripData = {
				name: data.tripTitle,
				input: {
					start: form.getValues().start,
					destination: form.getValues().destination,
					days: form.getValues().days,
				},
				loading: false,
				output: data,
			};

			if (newTrip) {
				// Create a new trip with a fresh id.
				const newTripId = Math.random().toString(36).substring(2, 9);
				useTripStore.setState((state) => ({
					trips: [...state.trips, { id: newTripId, ...tripData }],
					currentTripId: newTripId,
				}));
			} else {
				// Overwrite the existing trip.
				useTripStore.setState((state) => ({
					trips: state.trips.map((trip) =>
						trip.id === currentTripId
							? { ...trip, ...tripData }
							: trip,
					),
				}));
			}
		},
		onError: (error) => {
			console.error("Error during stream:", error.message);
			// Clear the assistant status if there's an error.
			setAssistantStatus("");
		},
	});

	// 4. Form submission handler.
	function onSubmit(values: TripValues) {
		mutation.mutate(values);
	}

	return (
		<div>
			<Form {...form}>
				<form
					onSubmit={form.handleSubmit(onSubmit)}
					className="space-y-8 px-2"
				>
					<FormField
						control={form.control}
						name="start"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Starting Location</FormLabel>
								<FormControl>
									<AutocompleteComponent
										{...field}
										automatic
									/>
								</FormControl>
								<FormDescription>
									This is where your road trip will begin.
								</FormDescription>
								<FormMessage />
							</FormItem>
						)}
					/>
					<FormField
						control={form.control}
						name="destination"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Final Destination</FormLabel>
								<FormControl>
									<AutocompleteComponent {...field} />
								</FormControl>
								<FormDescription>
									This is where your road trip will end.
								</FormDescription>
								<FormMessage />
							</FormItem>
						)}
					/>
					<FormField
						control={form.control}
						name="days"
						render={({ field }) => (
							<FormItem>
								<FormLabel>Number of Days</FormLabel>
								<FormControl>
									<Input
										type="number"
										placeholder="Enter number of days"
										{...field}
									/>
								</FormControl>
								<FormDescription>
									How many days will your trip take?
								</FormDescription>
								<FormMessage />
							</FormItem>
						)}
					/>
					{newTrip && (
						<Button
							type="submit"
							disabled={mutation.isPending}
							className="w-full"
						>
							{mutation.isPending ? "Loading…" : "Plan Trip"}
						</Button>
					)}
				</form>
			</Form>

			{!newTrip && <TripReportDialog />}

			{/* Display the assistant's current status if available */}
			{assistantStatus && (
				<div className="mt-4 p-4 border border-gray-300 rounded">
					<h2>Assistant Status:</h2>
					<p>{assistantStatus}</p>
				</div>
			)}
		</div>
	);
}
