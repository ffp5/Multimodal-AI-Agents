import "./globals.css";

import { Suspense, type ReactNode } from "react";
import StytchProvider from "@/components/StytchProvider";
import QueryClientContextProvider from "./QueryClientContextProvider";

export default function RootLayout({ children }: { children: ReactNode }) {
	return (
		<StytchProvider>
			<QueryClientContextProvider>
				<html lang="en">
					<title>Stytch Next.js App Router Example</title>
					<meta
						name="description"
						content="An example Next.js App Router application using Stytch for authentication"
					/>
					<body>
						<Suspense fallback={<div>Loading...</div>}>
							<main>{children}</main>
						</Suspense>
					</body>
				</html>
			</QueryClientContextProvider>
		</StytchProvider>
	);
}
