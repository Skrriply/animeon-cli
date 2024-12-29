import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class HTTPClient:
    """Client for making HTTP requests."""

    def __init__(self) -> None:
        """Initializes client with a new session."""
        self._session = requests.Session()

    def get(
        self,
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Makes a GET request to the specified URL.

        Args:
            url: URL to make the request to.
            params: Optional query parameters.
            headers: Optional request headers.

        Returns:
            Response data as JSON dict if successful.

        Raises:
            ConnectionError: If a connection error occurs.
            Timeout: If the request times out.
            HTTPError: If an HTTP error occurs.
            ValueError: If the response is not JSON.
        """
        try:
            with self._session as session:
                logger.debug(f"Виконується GET запит до {url}")
                logger.debug(f"Параметри: {params}")
                logger.debug(f"HTTP заголовки: {headers}")

                response = session.get(url, params=params, headers=headers)
                response.raise_for_status()

                logger.debug(f"Відповідь від сервера: {response.status_code}")
                return response.json()
        except requests.exceptions.ConnectionError as error:
            logger.error(f"Помилка з'єднання: {error}")
        except requests.exceptions.Timeout as error:
            logger.error(f"Час відповіді вичерпано: {error}")
        except requests.exceptions.HTTPError as error:
            logger.error(f"Не вдалося виконати запит: {error}")
        except ValueError as error:
            logger.error(f"Помилка декодування JSON: {error}")
