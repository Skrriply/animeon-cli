import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class HTTPClient:
    """Client for making HTTP requests."""

    def __init__(self) -> None:
        """Initializes the class."""
        self._session = requests.Session()

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        as_json: bool = True,
    ) -> Optional[Any]:
        """
        Makes a GET request to the specified URL.

        Args:
            url: URL to make the request to.
            params: Optional query parameters.
            headers: Optional request headers.
            timeout: Optional request timeout in seconds.
            as_json: Whether to return response as JSON.

        Returns:
            Response data as JSON dict or raw content if as_json is False.

        Raises:
            ConnectionError: If a connection error occurs.
            Timeout: If the request times out.
            HTTPError: If an HTTP error occurs.
            JSONDecodeError: If the response is not JSON when as_json is True.
        """
        logger.debug(f"Making GET request to {url}")
        logger.debug(f"Parameters: {params}")
        logger.debug(f"HTTP headers: {headers}")
        logger.debug(f"Timeout: {timeout}")

        try:
            with self._session as session:
                response = session.get(
                    url, params=params, headers=headers, timeout=timeout
                )
                response.raise_for_status()

                logger.debug(f"Server response: {response.status_code}")

                return response.json() if as_json else response.content
        except requests.exceptions.ConnectionError as error:
            logger.error(f"Connection error: {error}")
        except requests.exceptions.Timeout as error:
            logger.error(f"Request timed out: {error}")
        except requests.exceptions.HTTPError as error:
            logger.error(f"Failed to make request: {error}")
        except requests.exceptions.JSONDecodeError as error:
            logger.error(f"JSON decode error: {error}")
