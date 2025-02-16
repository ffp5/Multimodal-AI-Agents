"use client";

import React from "react";
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
import { AutocompleteComponent } from "./autocomplete";
import { formSchema } from "@/hooks/state/tripsStore";

// Derive our form values type from the zod schema.
type TripValues = z.infer<typeof formSchema>;

export function TripForm() {
	// Local state for streaming output.
	const [streamOutput, setStreamOutput] = React.useState<string>("");

	// 1. Define your form.
	const form = useForm<TripValues>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			start: "",
			destination: "",
			days: 1,
		},
	});

	// 2. Streaming request function.
	async function streamTripRequest(data: TripValues): Promise<string> {
		const response = await fetch("/api/trip", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(data),
		});

		if (!response.ok || !response.body) {
			throw new Error("Network error");
		}

		const reader = response.body.getReader();
		const decoder = new TextDecoder();
		let result = "";

		// Clear any existing output.
		setStreamOutput("");

		// Read stream chunks.
		while (true) {
			const { done, value } = await reader.read();
			if (done) break;
			const chunk = decoder.decode(value, { stream: true });
			result += chunk;
			// Append the chunk to our local streaming output.
			setStreamOutput((prev) => prev + chunk);
		}

		return result;
	}

	// 3. Use Tanstack Query mutation.
	const mutation = useMutation<string, Error, TripValues>({
		mutationFn: streamTripRequest,
		onMutate: () => {
			// Optionally, you can clear the streaming output here or set additional local loading state.
			setStreamOutput("");
		},
		onSuccess: (data) => {
			// You can use the final output here.
			// The streaming output has been built in the state already.
			console.log("Final output:", data);
		},
		onError: (error) => {
			// Handle errors appropriately.
			console.error("Error during stream:", error.message);
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
					<Button type="submit" disabled={mutation.isPending}>
						{mutation.isPending ? "Loading…" : "Submit"}
					</Button>
				</form>
			</Form>

			{/* Optionally display the streaming output */}
			{mutation.isPending && (
				<div className="mt-4">
					<h2>Streaming Output:</h2>
					<pre className="whitespace-pre-wrap bg-gray-100 p-4 rounded">
						{streamOutput}
					</pre>
				</div>
			)}
		</div>
	);
}
