import { NextRequest } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request: NextRequest) {
  // Get the backend URL from environment variables or use default
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';

  try {
    // Extract the request body
    const body = await request.json();

    // Get cookies to potentially forward to backend
    const cookieStore = cookies();
    const cookieHeader = cookieStore.toString();

    // Prepare headers, forwarding authentication and other important headers
    const headers: Record<string, string> = {};

    // Forward authentication-related headers
    const authHeaders = ['authorization', 'cookie'];
    for (const [key, value] of request.headers.entries()) {
      if (authHeaders.includes(key.toLowerCase())) {
        headers[key] = value;
      }
    }

    // If cookies weren't captured via the cookies() function, ensure they're included
    if (cookieHeader && !headers['cookie']) {
      headers['cookie'] = cookieHeader;
    }

    // Always include content-type for JSON requests
    headers['content-type'] = 'application/json';

    // Forward the request to the FastAPI backend
    const response = await fetch(`${backendUrl}/api/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });

    // Get the response data
    const responseData = await response.text();

    // Prepare response headers
    const responseHeaders = new Headers();
    responseHeaders.set('Content-Type', response.headers.get('content-type') || 'application/json');

    // Forward authentication-related headers from backend response
    const authResponseHeaders = ['set-cookie', 'authorization'];
    for (const [key, value] of response.headers.entries()) {
      if (authResponseHeaders.includes(key.toLowerCase()) && value) {
        responseHeaders.set(key, value);
      }
    }

    return new Response(responseData, {
      status: response.status,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error('Error forwarding request to backend:', error);

    return new Response(JSON.stringify({
      error: 'Failed to connect to backend service',
      message: error instanceof Error ? error.message : 'Unknown error'
    }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}