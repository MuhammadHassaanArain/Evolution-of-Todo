import { NextRequest } from 'next/server';
import { cookies } from 'next/headers';

// This handles GET requests to /api/conversations/[id]/messages
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  // Get the backend URL from environment variables or use default
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
  const conversationId = params.id;

  try {
    // Get cookies to potentially forward to backend
    const cookieStore = cookies();
    const cookieHeader = cookieStore.toString();

    // Prepare headers, forwarding authentication-related headers
    const headers: Record<string, string> = {};

    // Get authorization header if present
    const authHeader = request.headers.get('authorization');
    if (authHeader) {
      headers['authorization'] = authHeader;
    }

    // Include cookies if available
    if (cookieHeader) {
      headers['cookie'] = cookieHeader;
    }

    // Always include content-type for JSON requests
    headers['content-type'] = 'application/json';

    // Forward the request to the FastAPI backend
    const response = await fetch(`${backendUrl}/api/conversations/${conversationId}/messages`, {
      method: 'GET',
      headers,
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