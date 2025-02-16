import { AppSidebar } from "@/components/app-sidebar";
import Header from "@/components/trip/header";
import GoogleMapsDirections from "@/components/trip/maps/GoogleMapsDirections";

import {
	SidebarInset,
	SidebarProvider,
	SidebarTrigger,
} from "@/components/ui/sidebar";

export default function Page() {
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
