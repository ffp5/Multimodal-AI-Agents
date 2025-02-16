"use client";

import React, { useState, useEffect, useCallback, useMemo } from "react";
import {
	useLoadScript,
	GoogleMap,
	DirectionsService,
	DirectionsRenderer,
} from "@react-google-maps/api";
import { useTripStore } from "@/hooks/state/tripsStore";

// Define the container style.
const containerStyle = { width: "100%", height: "100%" };

// Define the libraries to load.
const libraries: "places"[] = ["places"];

// A default/fallback location (example: SF)
const fallbackCenter = { lat: 37.7749, lng: -122.4194 };

// Main component.
const GoogleMapsDirections: React.FC = () => {
	const trips = useTripStore((state) => state.trips);
	const currentTripId = useTripStore((state) => state.currentTripId);
	const currentTrip = useMemo(() => {
		return trips.find((trip) => trip.id === currentTripId);
	}, [trips, currentTripId]);

	const { isLoaded } = useLoadScript({
		googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? "",
		libraries,
	});

	// State to keep track of the map center.
	const [center, setCenter] = useState<{ lat: number; lng: number }>(
		fallbackCenter,
	);

	// Store the directions result.
	const [directions, setDirections] =
		useState<google.maps.DirectionsResult | null>(null);

	// Callback for the DirectionsService.
	const directionsCallback = useCallback(
		(
			response: google.maps.DirectionsResult | null,
			status: google.maps.DirectionsStatus,
		) => {
			if (response !== null && status === "OK") {
				// Set directions only once to prevent re-render loops.
				if (!directions) {
					setDirections(response);
				}
			} else if (status !== "OK") {
				console.error(`Directions request failed due to ${status}`);
			} else {
				console.log(`Unknown error: ${status}`);
			}
		},
		[directions],
	);

	// Reset directions whenever the trip changes.
	useEffect(() => {
		setDirections(null);
	}, [currentTrip]);

	// Try to get the user's current location.
	useEffect(() => {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				(position) => {
					setCenter({
						lat: position.coords.latitude,
						lng: position.coords.longitude,
					});
				},
				(error) => {
					console.error(
						"Error fetching geolocation, using fallback",
						error,
					);
					// Here you might try to fetch an approximate location from IP-based services.
					// Example: fetch approximate location using your own API or a third party service.
				},
			);
		}
	}, []);

	// Compute the path (list of locations).
	const PATH = useMemo(() => {
		return currentTrip?.output?.days.map((step) => step.location) ?? [];
	}, [currentTrip]);

	// Prepare the waypoints from PATH (all elements between the first and the last)
	const waypoints = useMemo(() => {
		return PATH.length > 2
			? PATH.slice(1, PATH.length - 1).map((city) => ({
					location: city,
					stopover: true,
				}))
			: [];
	}, [PATH]);

	return (
		<>
			{isLoaded && (
				<GoogleMap
					mapContainerStyle={containerStyle}
					zoom={10}
					center={center}
				>
					{/* Only trigger the DirectionsService if directions have not been set yet and the path exists */}
					{!directions && PATH.length > 0 && (
						<DirectionsService
							options={{
								origin: PATH[0],
								destination: PATH[PATH.length - 1],
								waypoints: waypoints,
								travelMode: google.maps.TravelMode.DRIVING,
							}}
							callback={(result, status) =>
								directionsCallback(result, status)
							}
						/>
					)}
					{directions && (
						<DirectionsRenderer
							options={{
								directions: directions,
							}}
						/>
					)}
				</GoogleMap>
			)}
		</>
	);
};

export default React.memo(GoogleMapsDirections);
