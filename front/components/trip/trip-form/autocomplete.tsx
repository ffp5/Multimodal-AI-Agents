"use client";

import type React from "react";
import { type ChangeEventHandler, useState, useEffect } from "react";
import { useLoadScript } from "@react-google-maps/api";
import AddressAutoComplete, {
	type AddressType,
} from "@/components/ui/address-autocomplete";

interface Props {
	value: string;
	onChange: ChangeEventHandler<HTMLInputElement>;
	onBlur: () => void;
	name: string;
	ref: React.Ref<HTMLInputElement>;
	automatic?: boolean;
}

/**
 * Uses Google's Geocoding API to reverse geocode the given coordinates.
 * This function returns a promise that resolves to an AddressType.
 */
function fetchAddressFromCoordinates(
	lat: number,
	lng: number,
): Promise<AddressType> {
	return new Promise((resolve, reject) => {
		const googleObj = (window as any).google;
		if (!googleObj || !googleObj.maps) {
			reject("Google Maps JavaScript API is not loaded.");
			return;
		}

		const geocoder = new googleObj.maps.Geocoder();
		geocoder.geocode(
			{ location: { lat, lng } },
			(results: any, status: any) => {
				if (
					status === googleObj.maps.GeocoderStatus.OK &&
					results &&
					results.length > 0
				) {
					const result = results[0];

					// Prepare a basic AddressType. Customize further if needed.
					const address: AddressType = {
						address1: result.formatted_address,
						address2: "",
						formattedAddress: result.formatted_address,
						city: "",
						region: "",
						postalCode: "",
						country: "",
						lat,
						lng,
					};

					for (const comp of result.address_components as any[]) {
						if (comp.types.includes("locality")) {
							address.city = comp.long_name;
						}
						if (
							comp.types.includes("administrative_area_level_1")
						) {
							address.region = comp.short_name;
						}
						if (comp.types.includes("postal_code")) {
							address.postalCode = comp.long_name;
						}
						if (comp.types.includes("country")) {
							address.country = comp.long_name;
						}
					}

					resolve(address);
				} else {
					reject(`Geocoder failed due to: ${status}`);
				}
			},
		);
	});
}

export const AutocompleteComponent = (props: Props) => {
	const { automatic = false } = props;
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
	const [searchInput, setSearchInput] = useState("");

	const { isLoaded, loadError } = useLoadScript({
		googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? "",
		libraries: ["places"],
	});

	useEffect(() => {
		if (automatic && isLoaded && navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				async (position) => {
					const { latitude, longitude } = position.coords;
					try {
						const autoAddress = await fetchAddressFromCoordinates(
							latitude,
							longitude,
						);
						setAddress(autoAddress);
						setSearchInput(autoAddress.formattedAddress);
						props.onChange({
							// @ts-expect-error - synthetic event shape
							target: {
								name: "address",
								value: autoAddress.formattedAddress,
							},
						});
					} catch (error) {
						console.error(
							"Error fetching address from coordinates:",
							error,
						);
					}
				},
				(error) => {
					console.error("Geolocation error:", error);
				},
			);
		}
	}, [automatic, isLoaded]);

	if (loadError) {
		return <div>Error loading Google Maps API</div>;
	}

	if (!isLoaded) {
		return <div>Loading...</div>;
	}

	return (
		<AddressAutoComplete
			address={address}
			setAddress={setAddress}
			searchInput={searchInput}
			setSearchInput={setSearchInput}
			dialogTitle="Enter Address"
			updateWithCurrentLocation={automatic} // Pass the flag here
			{...props}
		/>
	);
};
