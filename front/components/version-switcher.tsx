"use client";

import React from "react";
import { Check, ChevronsUpDown, GalleryVerticalEnd } from "lucide-react";

import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useTripStore } from "@/hooks/state/tripsStore";

export function TripSwitcher() {
	// Instead of using computed getters from the store,
	// read the state properties directly.
	const trips = useTripStore((state) => state.trips);
	const currentTripId = useTripStore((state) => state.currentTripId);
	const currentTrip = React.useMemo(() => {
		return trips.find((trip) => trip.id === currentTripId);
	}, [trips, currentTripId]);

	// Append the "New Trip" entry inside the component.
	const tripsWithNew = React.useMemo(() => {
		const newTrip = {
			id: "-1",
			name: "New Trip",
			input: { start: "", destination: "", days: 1 },
			loading: false,
		};
		return [...trips, newTrip];
	}, [trips]);

	return (
		<SidebarMenu>
			<SidebarMenuItem>
				<DropdownMenu>
					<DropdownMenuTrigger asChild>
						<SidebarMenuButton
							size="lg"
							className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
						>
							<div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
								<GalleryVerticalEnd className="size-4" />
							</div>
							<div className="flex flex-col gap-0.5 leading-none">
								<span className="font-semibold">Trips</span>
								<span>{currentTrip?.name ?? "New Trip"}</span>
							</div>
							<ChevronsUpDown className="ml-auto" />
						</SidebarMenuButton>
					</DropdownMenuTrigger>
					<DropdownMenuContent
						className="w-[--radix-dropdown-menu-trigger-width]"
						align="start"
					>
						{tripsWithNew.map((trip) => (
							<DropdownMenuItem
								key={trip.id}
								onSelect={() => {
									// Only update if the selected trip is different.
									if (trip.id !== currentTrip?.id) {
										useTripStore.setState({
											currentTripId: trip.id,
										});
									}
								}}
							>
								{trip.name}
								{trip.id === currentTrip?.id && (
									<Check className="ml-auto" />
								)}
							</DropdownMenuItem>
						))}
					</DropdownMenuContent>
				</DropdownMenu>
			</SidebarMenuItem>
		</SidebarMenu>
	);
}
