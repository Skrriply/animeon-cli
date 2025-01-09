def normalize_query(query: str) -> str:
    """
    Normalizes query for URL encoding.

    Args:
        query: Query to normalize.

    Returns:
        Normalized query.
    """
    replacements = {
        "/": "",  # Removed because server returns status code 500 when used
        "\\": "%5C",
        "?": "%3F",
        "#": "%23",
        "&": "%26",
        "=": "%3D",
        " ": "%20",
    }

    query = query.strip()
    for char, replacement in replacements.items():
        query = query.replace(char, replacement)

    return query


def build_url(base_url: str, endpoint: str) -> str:
    """
    Builds URL from base URL and endpoint.

    Args:
        base_url: Base URL.
        endpoint: Endpoint.

    Returns:
        Built URL.
    """
    return f"{base_url}/{endpoint}"
