import type { formSchema, Trip } from "@/hooks/state/tripsStore";
import type { z } from "zod";

export function isNewTrip(
	current: Trip | undefined,
	next: z.infer<typeof formSchema>,
) {
	// Deep comparison between current and next trips
	return (
		JSON.stringify(current?.input) !== JSON.stringify(next) ||
		!current?.output
	);
}
