"use client";

import React, { useState, useEffect } from "react";
import { useLoadScript } from "@react-google-maps/api";
import AddressAutoComplete from "./AddressAutoComplete";
import { fetchAddressFromCoordinates } from "@/utils/address"; // your helper

export interface AddressType {
	address1: string;
	address2: string;
	formattedAddress: string;
	city: string;
	region: string;
	postalCode: string;
	country: string;
	lat: number;
	lng: number;
	placeId?: string;
}

interface AutocompleteComponentProps {
	value: string;
	onChange: React.ChangeEventHandler<HTMLInputElement>;
	onBlur: () => void;
	name: string;
	automatic?: boolean;
}

export const AutocompleteComponent = (props: AutocompleteComponentProps) => {
	const { automatic = false, value, onChange, onBlur, name } = props;
	const { isLoaded, loadError } = useLoadScript({
		googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? "",
		libraries: ["places"],
	});

	// The source-of-truth for the detailed address info.
	const [address, setAddress] = useState<AddressType>({
		address1: "",
		address2: "",
		formattedAddress: "",
		city: "",
		region: "",
		postalCode: "",
		country: "",
		lat: 0,
		lng: 0,
	});
	// This controls what’s shown in the input.
	const [searchInput, setSearchInput] = useState(value || "");
	// To ensure we only run geolocation once.
	const [hasAutoFetched, setHasAutoFetched] = useState(false);

	// 1. Auto-fetch address from geolocation when no value is provided.
	useEffect(() => {
		if (
			automatic &&
			!value &&
			!hasAutoFetched &&
			isLoaded &&
			navigator.geolocation
		) {
			navigator.geolocation.getCurrentPosition(async (position) => {
				const { latitude, longitude } = position.coords;
				try {
					const autoAddress = await fetchAddressFromCoordinates(
						latitude,
						longitude,
					);
					setAddress(autoAddress);
					setSearchInput(autoAddress.formattedAddress);
					// Notify parent about the auto-filled address.
					onChange({
						target: { name, value: autoAddress.formattedAddress },
					} as any);
					setHasAutoFetched(true);
				} catch (error) {
					console.error("Error auto-fetching address:", error);
				}
			});
		}
	}, [automatic, value, hasAutoFetched, isLoaded, name, onChange]);

	// 2. If an address value is provided (controlled mode), update the search input.
	// You might also trigger a details fetch here if needed.
	useEffect(() => {
		if (value && value !== address.formattedAddress) {
			setSearchInput(value);
			// Optionally: fetch address details if you only have an ID.
			// For simplicity we assume the value is the formatted address.
		}
		// We intentionally don’t update the address state here to avoid loops.
	}, [value, address.formattedAddress]);

	if (loadError) return <div>Error loading Google Maps API</div>;
	if (!isLoaded) return <div>Loading Maps...</div>;

	return (
		<AddressAutoComplete
			value={value}
			onChange={onChange}
			onBlur={onBlur}
			name={name}
			address={address}
			setAddress={setAddress}
			searchInput={searchInput}
			setSearchInput={setSearchInput}
			automatic={automatic}
		/>
	);
};

export default AutocompleteComponent;
