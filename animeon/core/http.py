import logging
from typing import Any, Dict, Optional

import requests
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    JSONDecodeError,
    Timeout,
)

logger = logging.getLogger(__name__)


class HTTPClient:
    """Client for making HTTP requests."""

    def __init__(self) -> None:
        """Initializes the class."""
        self.session = requests.Session()

    @staticmethod
    def _handle_error(error: Exception) -> None:
        """
        Handles an error by logging it.

        Args:
            error: The error to handle.
        """
        if isinstance(error, ConnectionError):
            logger.error(f"Connection error: {error}")
        elif isinstance(error, Timeout):
            logger.error(f"Request timed out: {error}")
        elif isinstance(error, HTTPError):
            logger.error(f"Failed to make request: {error}")
        elif isinstance(error, JSONDecodeError):
            logger.error(f"JSON decode error: {error}")

    def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> Optional[requests.Response]:
        """
        Makes a request to the specified URL.

        Args:
            method: HTTP method to use.
            url: URL to make the request to.
            params: Optional parameters to include in the request.
            headers: Optional headers to include in the request.
            timeout: Optional timeout for the request.

        Returns:
            Response from the request if successful, None otherwise.
        """
        try:
            response = self.session.request(
                method, url, params=params, headers=headers, timeout=timeout
            )
            response.raise_for_status()
            return response
        except (ConnectionError, Timeout, HTTPError, JSONDecodeError) as error:
            self._handle_error(error)
            return None

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> Optional[requests.Response]:
        """
        Makes a GET request to the specified URL.

        Args:
            url: URL to make the request to.
            params: Optional parameters to include in the request.
            headers: Optional headers to include in the request.
            timeout: Optional timeout for the request.

        Returns:
            Response from the request if successful, None otherwise.
        """
        return self._request(
            "GET", url, params=params, headers=headers, timeout=timeout
        )
