import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui/dialog";
import { useTripStore } from "@/hooks/state/tripsStore";
import { useMemo } from "react";

export const TripReportDialog = () => {
	const trips = useTripStore((state) => state.trips);
	const currentTripId = useTripStore((state) => state.currentTripId);
	const currentTrip = useMemo(() => {
		return trips.find((trip) => trip.id === currentTripId);
	}, [trips, currentTripId]);

	return (
		<Dialog>
			<DialogTrigger className="w-full p-2">
				<Button className="w-full">See Trip Details</Button>
			</DialogTrigger>
			<DialogContent>
				<DialogHeader>
					<DialogTitle className="text-center text-2xl">
						{currentTrip?.name || "No Trip Selected"}
					</DialogTitle>
					<DialogDescription>
						This is a trip report dialog.
					</DialogDescription>
				</DialogHeader>
			</DialogContent>
		</Dialog>
	);
};
