import "./globals.css";

import { Suspense, type ReactNode } from "react";
import StytchProvider from "@/components/StytchProvider";
import QueryClientContextProvider from "./QueryClientContextProvider";
import { Toaster } from "@/components/ui/sonner";

export default function RootLayout({ children }: { children: ReactNode }) {
	return (
		<StytchProvider>
			<QueryClientContextProvider>
				<html lang="en">
					<title>🌍 Trip Planner</title>
					<meta
						name="description"
						content="AI Agent Hackathon - Trip Planner"
					/>
					<body>
						<Suspense fallback={<div>Loading...</div>}>
							<main>{children}</main>
						</Suspense>
						<Toaster />
					</body>
				</html>
			</QueryClientContextProvider>
		</StytchProvider>
	);
}
