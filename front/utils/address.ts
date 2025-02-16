import { AddressType } from "@/components/ui/address-autocomplete";

/**
 * Uses Google's Geocoding API to reverse geocode the given coordinates.
 * This function returns a promise that resolves to an AddressType.
 */
export function fetchAddressFromCoordinates(
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
