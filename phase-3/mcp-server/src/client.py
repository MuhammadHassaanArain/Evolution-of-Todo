"""HTTP client module for backend API calls."""

import httpx
import os
from typing import Dict, Any, Optional
from .config import settings


class BackendAPIClient:
    """Client for making HTTP requests to the backend API."""

    def __init__(self):
        self.base_url = settings.backend_api_url
        self.timeout = settings.backend_api_timeout

    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for requests, including authentication if available."""
        headers = {"Content-Type": "application/json"}

        # Add authentication header if provided via environment variable
        auth_token = os.getenv("AUTHORIZATION_TOKEN")
        if auth_token:
            headers["Authorization"] = auth_token

        return headers

    def _merge_headers(self, provided_headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Merge provided headers with default headers."""
        default_headers = self._get_default_headers()
        if provided_headers:
            default_headers.update(provided_headers)
        return default_headers

    async def make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the backend API.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint (e.g., '/api/tasks')
            headers: Optional headers to include in the request
            json_data: Optional JSON payload for the request

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"

        # Merge provided headers with default headers
        merged_headers = self._merge_headers(headers)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=merged_headers,
                json=json_data
            )

            # Raise an exception for bad status codes
            response.raise_for_status()

            # Return the JSON response
            return response.json()

    async def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make a GET request to the backend API."""
        return await self.make_request("GET", endpoint, headers)

    async def post(self, endpoint: str, headers: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request to the backend API."""
        return await self.make_request("POST", endpoint, headers, json_data)

    async def put(self, endpoint: str, headers: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request to the backend API."""
        return await self.make_request("PUT", endpoint, headers, json_data)

    async def patch(self, endpoint: str, headers: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request to the backend API."""
        return await self.make_request("PATCH", endpoint, headers, json_data)

    async def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make a DELETE request to the backend API."""
        return await self.make_request("DELETE", endpoint, headers)


# Global client instance
backend_client = BackendAPIClient()