"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

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

const formSchema = z.object({
	start: z.string().min(2, {
		message: "Starting location must be at least 2 characters.",
	}),
	destination: z.string().min(2, {
		message: "Destination must be at least 2 characters.",
	}),
	days: z
		.number({ invalid_type_error: "Number of days is required" })
		.min(1, {
			message: "There must be at least 1 day for the trip.",
		}),
});

export function TripForm() {
	// 1. Define your form.
	const form = useForm<z.infer<typeof formSchema>>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			start: "",
			destination: "",
			days: 1,
		},
	});

	// 2. Define a submit handler.
	function onSubmit(values: z.infer<typeof formSchema>) {
		// Do something with the form values.
		// ✅ This will be type-safe and validated.
		console.log(values);
	}
	return (
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
								<AutocompleteComponent {...field} />
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
				<Button type="submit">Submit</Button>
			</form>
		</Form>
	);
}
