import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui/dialog";
import {
	type TripOutputSchema,
	useTripStore,
	type OtherActivitySchema,
} from "@/hooks/state/tripsStore";
import type { z } from "zod";

// Infer types from the schema
type TripData = z.infer<typeof TripOutputSchema>;
type DayData = TripData["days"][number];
type ActivityData = z.infer<typeof OtherActivitySchema>;
type HotelData = DayData["hotel"];
type CarRentalData = TripData["carRental"];

// Mapping of activity types to icons/emojis
const ACTIVITY_ICONS: Record<string, string> = {
	sightseeing: "🏛️",
	culinary: "🍽️",
	adventure: "🏃‍♂️",
	hiking: "🥾",
	camping: "⛺",
	museum: "🏛️",
	landmark: "🗽",
	shopping: "🛍️",
	"local-market": "🏪",
	"cultural-tour": "🎭",
	wildlife: "🦁",
	beach: "🏖️",
	"scenic-drive": "🚗",
	"historical-exploration": "📜",
	"photo-op": "📸",
	"wine-tasting": "🍷",
	gastronomic: "👨‍🍳",
	"local-festival": "🎪",
	relaxation: "🧘‍♀️",
	"sporting-activities": "⚽",
	car: "🚗",
};

const ActivityItem = ({ activity }: { activity: ActivityData }) => {
	const icon = ACTIVITY_ICONS[activity.type] || "📍";

	return (
		<div className="border-b border-gray-100 py-4 px-4 last:border-none">
			<div className="flex items-start gap-4">
				<span className="text-2xl">{icon}</span>
				<div className="flex-1">
					<div className="flex justify-between items-center">
						{activity.name && (
							<h4 className="font-medium text-lg">
								{activity.name}
							</h4>
						)}
						{activity.schedule && (
							<span className="text-sm text-gray-500">
								{activity.schedule.start} -{" "}
								{activity.schedule.end}
							</span>
						)}
					</div>
					<p className="text-gray-600 mt-1">{activity.description}</p>
					{
						//@ts-expect-error - Car
						activity.type === "car" && activity.durationSeconds && (
							<div className="mt-2 text-sm text-gray-500">
								Duration:{" "}
								{
									//@ts-expect-error - Car
									Math.floor(activity.durationSeconds / 3600)
								}
								h{" "}
								{Math.floor(
									//@ts-expect-error - Car
									(activity.durationSeconds % 3600) / 60,
								)}
								m
							</div>
						)
					}
				</div>
			</div>
		</div>
	);
};

const HotelCard = ({ hotel }: { hotel: HotelData }) => {
	return (
		<div className="flex gap-6 p-4 border rounded-lg shadow-sm">
			{hotel.image ? (
				<img
					src={hotel.image}
					alt={hotel.name}
					className="w-32 h-32 rounded-lg object-cover"
				/>
			) : (
				<div className="w-32 h-32 bg-gray-100 rounded-lg flex items-center justify-center">
					🏨
				</div>
			)}
			<div className="flex-1">
				<h3 className="text-xl font-semibold">{hotel.name}</h3>
				<p className="text-gray-600 mt-1">{hotel.address}</p>
				<div className="mt-2">
					{Array.from({ length: hotel.stars }).map((_, i) => (
						<span key={i} className="text-yellow-400">
							⭐
						</span>
					))}
				</div>
			</div>
		</div>
	);
};

const DayCard = ({ day, isLastDay }: { day: DayData; isLastDay: boolean }) => {
	// Find a car activity if exists (for traveling to next city)
	const carActivity = day.activities.find(
		(activity) => activity.type === "car",
	);

	return (
		<div className="mb-8">
			<div className="flex items-center gap-4 mb-4">
				<div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full font-medium">
					Day {day.dayNumber}
				</div>
				<h2 className="text-2xl font-bold">{day.location}</h2>
			</div>

			<p className="text-gray-600 mb-6">{day.description}</p>

			<div className="space-y-6">
				<section>
					<h3 className="text-lg font-semibold mb-4">Activities</h3>
					<div className="bg-white rounded-lg border">
						{day.activities.map(
							(activity, idx) =>
								activity.type !== "car" && (
									<ActivityItem
										key={idx}
										activity={activity}
									/>
								),
						)}
					</div>
				</section>

				<section>
					<h3 className="text-lg font-semibold mb-4">
						Accommodation
					</h3>
					<HotelCard hotel={day.hotel} />
				</section>

				{!isLastDay && carActivity && (
					<section>
						<h3 className="text-lg font-semibold mb-4">
							Travel to Next Destination
						</h3>
						<div className="bg-white rounded-lg border">
							<ActivityItem activity={carActivity as any} />
						</div>
					</section>
				)}

				{day.notes && (
					<section className="bg-amber-50 p-4 rounded-lg border border-amber-100">
						<h4 className="font-medium mb-2">📝 Notes</h4>
						<p className="text-gray-700">{day.notes}</p>
					</section>
				)}
			</div>
		</div>
	);
};

const CarRentalCard = ({ carRental }: { carRental: CarRentalData }) => {
	return (
		<div className="p-4 border rounded-lg shadow-sm bg-white">
			<h3 className="text-xl font-semibold mb-1">Car Rental Details</h3>
			<p className="text-sm">
				<strong>Company:</strong> {carRental.company}
			</p>
			<p className="text-sm">
				<strong>Pickup:</strong> {carRental.pickupLocation} at{" "}
				{new Date(carRental.pickupDateTime).toLocaleString()}
			</p>
			<p className="text-sm">
				<strong>Return:</strong> {carRental.returnLocation} at{" "}
				{new Date(carRental.returnDateTime).toLocaleString()}
			</p>
			<p className="text-sm">
				<strong>Vehicle Type:</strong> {carRental.vehicleType}
			</p>
			<p className="text-sm">
				<strong>Rate:</strong> {carRental.dailyRate}{" "}
				{carRental.currency} per day
			</p>
			<p className="text-sm">
				<strong>Extras:</strong>{" "}
				{carRental.extras.insuranceIncluded
					? "Insurance Included"
					: "No Insurance"}
				, {carRental.extras.mileageLimit}
			</p>
			<p className="text-xs text-gray-500">{carRental.extras.notes}</p>
		</div>
	);
};

export const TripReportDialog = () => {
	const trips = useTripStore((state) => state.trips);
	const currentTripId = useTripStore((state) => state.currentTripId);
	const currentTrip = trips.find((trip) => trip.id === currentTripId);

	// Ensure we use the typed output from the TripSchema
	const tripData: TripData | undefined = currentTrip?.output;

	return (
		<Dialog>
			<DialogTrigger className="w-full p-2">
				<Button className="w-full">See Trip Details</Button>
			</DialogTrigger>
			<DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
				<DialogHeader className="mb-8">
					<DialogTitle className="text-3xl font-bold text-center">
						{tripData?.tripTitle || "No Trip Selected"}
					</DialogTitle>
					<p className="text-center text-gray-600 mt-2">
						{tripData.tripOverview.description}
					</p>
				</DialogHeader>

				{tripData ? (
					<div className="px-6">
						{tripData.days.map((day, index) => (
							<DayCard
								key={index}
								day={day}
								isLastDay={index === tripData.days.length - 1}
							/>
						))}

						<div className="mb-6">
							<h2 className="text-2xl font-bold mb-2">
								Car Rental Information
							</h2>
							<CarRentalCard carRental={tripData.carRental} />
						</div>
					</div>
				) : (
					<p className="text-center text-gray-500">
						No trip details available.
					</p>
				)}
			</DialogContent>
		</Dialog>
	);
};
