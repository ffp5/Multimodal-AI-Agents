import { type NextRequest, NextResponse } from "next/server";

const TARGET = "http://10.20.7.222:5000/plan-trip-stream";

/**
 * A helper function that forwards the incoming NextRequest to the target server.
 *
 * It removes the `/api/trip` prefix from the pathname so that a request
 * to `/api/trip/some/path` is forwarded to `http://10.20.7.222:5000/some/path`.
 */
async function proxy(request: NextRequest): Promise<Response> {
	const requestUrl = new URL(request.url);

	// Remove the "/api/trip" prefix from the path.
	let pathname = requestUrl.pathname.replace(/^\/api\/trip/, "");
	if (!pathname || pathname === "") pathname = "/";

	// Construct the target URL including query parameters.
	const targetUrl = TARGET + pathname + requestUrl.search;

	// Clone and modify headers if necessary.
	const headers = new Headers(request.headers);
	headers.set("host", new URL(TARGET).host);

	// Forward the request. Note the inclusion of `duplex: 'half'` is required
	// when streaming the request body.
	const response = await fetch(targetUrl, {
		method: request.method,
		headers,
		body: request.body, // Use the stream (if available) for non-GET/HEAD methods.
		duplex: "half",
	});

	// Return a streaming response.
	return new Response(response.body, {
		status: response.status,
		headers: response.headers,
	});
}

// Export handlers for the common HTTP methods.
// You can add or remove methods depending on your use case.
export async function GET(request: NextRequest) {
	return proxy(request);
}

export async function POST(request: NextRequest) {
	return proxy(request);
}

export async function PUT(request: NextRequest) {
	return proxy(request);
}

export async function PATCH(request: NextRequest) {
	return proxy(request);
}

export async function DELETE(request: NextRequest) {
	return proxy(request);
}

export async function OPTIONS(request: NextRequest) {
	return proxy(request);
}
