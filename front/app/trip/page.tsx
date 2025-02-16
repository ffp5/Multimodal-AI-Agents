"use client";

import { AppSidebar } from "@/components/app-sidebar";
import Header from "@/components/trip/header";
import GoogleMapsDirections from "@/components/trip/maps/GoogleMapsDirections";

import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { useStytchUser } from "@stytch/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Page() {
	const { user, isInitialized } = useStytchUser();
	const router = useRouter();
	// If the Stytch SDK detects a User then redirect to profile; for example if a logged in User navigated directly to this URL.
	useEffect(() => {
		if (isInitialized && !user) {
			router.replace("/");
		}
	}, [user, isInitialized, router]);

	return (
		<SidebarProvider>
			<AppSidebar />
			<SidebarInset>
				<Header />
				<div className="flex flex-1 flex-col gap-4 h-full w-full google-maps">
					<GoogleMapsDirections />
				</div>
			</SidebarInset>
		</SidebarProvider>
	);
}
