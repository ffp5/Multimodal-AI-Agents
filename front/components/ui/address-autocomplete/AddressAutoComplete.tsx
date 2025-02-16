"use client";

import type React from "react";
import { useState, useCallback, useEffect } from "react";
import { useDebounce } from "@/hooks/use-debounce";
import { fetcher } from "@/utils/fetcher";
import { Input } from "@/components/ui/input";
import type { AddressType } from "./AutocompleteComponent";

export interface AddressAutoCompleteProps {
	address: AddressType;
	setAddress: (address: AddressType) => void;
	searchInput: string;
	setSearchInput: (value: string) => void;
	value: string;
	onChange: React.ChangeEventHandler<HTMLInputElement>;
	onBlur: () => void;
	name: string;
	automatic?: boolean;
}

export default function AddressAutoComplete(props: AddressAutoCompleteProps) {
	const { setAddress, searchInput, setSearchInput, onChange, onBlur, name } =
		props;

	// State to track if the user is editing the address.
	const [isEditing, setIsEditing] = useState(false);
	// State to store autocomplete predictions.
	const [predictions, setPredictions] = useState<any[]>([]);
	// Debounced input value to limit prediction fetch calls.
	const debouncedInput = useDebounce(searchInput, 500);

	// Fetch predictions when the debounced input changes.
	useEffect(() => {
		if (debouncedInput.trim() !== "") {
			fetcher(`/api/address/autocomplete?input=${debouncedInput}`)
				.then((res) => {
					setPredictions(res.data || []);
				})
				.catch((error) =>
					console.error("Error fetching predictions:", error),
				);
		} else {
			setPredictions([]);
		}
	}, [debouncedInput]);

	// Handler when a prediction is selected.
	const handleSelect = useCallback(
		(prediction: any) => {
			// Extract the formatted address from the prediction.
			const formattedAddress = prediction.placePrediction.text.text;
			const selectedAddress: AddressType = {
				address1: formattedAddress,
				address2: "",
				formattedAddress, // The full address text.
				city: "",
				region: "",
				postalCode: "",
				country: "",
				lat: 0,
				lng: 0,
				placeId: prediction.placePrediction.placeId,
			};
			// Update the detailed address state.
			setAddress(selectedAddress);
			// Update the search input to reflect the chosen address.
			setSearchInput(selectedAddress.formattedAddress);
			// Notify the parent component of the change.
			onChange({
				target: { name, value: selectedAddress.formattedAddress },
			} as any);
			onBlur();
			setIsEditing(false);
		},
		[name, onBlur, onChange, setAddress, setSearchInput],
	);

	// // Handler to clear the current address.
	// const clearAddress = useCallback(() => {
	// 	setAddress({
	// 		address1: "",
	// 		address2: "",
	// 		formattedAddress: "",
	// 		city: "",
	// 		region: "",
	// 		postalCode: "",
	// 		country: "",
	// 		lat: 0,
	// 		lng: 0,
	// 	});
	// 	setSearchInput("");
	// 	onChange({
	// 		target: { name, value: "" },
	// 	} as any);
	// }, [name, onChange, setAddress, setSearchInput]);

	return (
		<div className="relative">
			{/* When not editing, display a read-only input with edit and clear buttons */}
			{!isEditing ? (
				<div className="flex items-center gap-2">
					<Input
						readOnly
						value={searchInput}
						name={name}
						onFocus={() => setIsEditing(true)}
						onClick={() => setIsEditing(true)}
					/>
				</div>
			) : (
				// Editing state: show the input with autocomplete suggestions.
				<div className="relative">
					<Input
						autoFocus
						value={searchInput}
						name={name}
						onChange={(e) => {
							setSearchInput(e.target.value);
							onChange(e);
						}}
						onBlur={() => {
							// Delay closing to allow suggestion clicks.
							setTimeout(() => {
								setIsEditing(false);
								onBlur();
							}, 150);
						}}
						placeholder="Enter address"
					/>
					{/* Display suggestions if there are any */}
					{debouncedInput && predictions.length > 0 && (
						<ul className="absolute z-50 w-full border bg-white shadow-lg">
							{predictions.map((prediction: any) => (
								<li
									key={prediction.placePrediction.placeId}
									className="p-2 hover:bg-gray-100 cursor-pointer"
									onMouseDown={(e) => e.preventDefault()}
									onClick={() => handleSelect(prediction)}
								>
									{prediction.placePrediction.text.text}
								</li>
							))}
						</ul>
					)}
					{/* Fallback when no predictions are found */}
					{debouncedInput && predictions.length === 0 && (
						<div className="absolute z-50 w-full border bg-white shadow-lg p-2">
							No address found.
						</div>
					)}
				</div>
			)}
		</div>
	);
}
