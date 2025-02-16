"use client";
import {
	Breadcrumb,
	BreadcrumbItem,
	BreadcrumbLink,
	BreadcrumbList,
	BreadcrumbPage,
	BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "../ui/sidebar";
import { useTripStore } from "@/hooks/state/tripsStore";
import React from "react";
import { useStytch, useStytchUser } from "@stytch/nextjs";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { Link } from "lucide-react";
import { Avatar, AvatarImage, AvatarFallback } from "../ui/avatar";

function gravatar(email: string) {
	const hash = email
		.toLowerCase()
		.trim()
		.split("")
		.reduce((acc, char) => {
			return acc + char.charCodeAt(0);
		}, 0);
	return `https://www.gravatar.com/avatar/${hash}?d=identicon`;
}

export default function Header() {
	const { user, isInitialized } = useStytchUser();
	const stytch = useStytch();
	const trips = useTripStore((state) => state.trips);
	const currentTripId = useTripStore((state) => state.currentTripId);
	const currentTrip = React.useMemo(() => {
		return trips.find((trip) => trip.id === currentTripId);
	}, [trips, currentTripId]);
	return (
		<header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
			<SidebarTrigger className="-ml-1" />
			<Separator orientation="vertical" className="mr-2 h-4" />
			<div className="flex items-center justify-between w-full">
				<Breadcrumb>
					<BreadcrumbList>
						<BreadcrumbItem className="hidden md:block">
							<BreadcrumbLink href="#">Trip</BreadcrumbLink>
						</BreadcrumbItem>
						<BreadcrumbSeparator className="hidden md:block" />
						<BreadcrumbItem>
							<BreadcrumbPage>
								{currentTrip?.name || "New Trip"}
							</BreadcrumbPage>
						</BreadcrumbItem>
					</BreadcrumbList>
				</Breadcrumb>
				<DropdownMenu>
					<DropdownMenuTrigger>
						<Avatar>
							<AvatarImage
								src={gravatar(user?.emails[0].email ?? "")}
							/>
							<AvatarFallback>
								{user?.name.first_name[0]}
								{user?.name.last_name[0]}
							</AvatarFallback>
						</Avatar>
					</DropdownMenuTrigger>
					<DropdownMenuContent>
						<DropdownMenuItem>
							{user?.emails[0].email}
						</DropdownMenuItem>
						<DropdownMenuItem
							onClick={() => stytch.session.revoke()}
						>
							Sign Out
						</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>
			</div>
		</header>
	);
}
