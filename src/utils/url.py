def normalize_query(query: str) -> str:
    """
    Normalizes query for URL encoding.

    Args:
        query: Query to normalize.

    Returns:
        Normalized query.
    """
    query = query.strip()
    # Character "/" is removed because server returns status code 500 when used
    query = query.replace("/", "")
    query = query.replace("\\", "%5C")
    query = query.replace("?", "%3F")
    query = query.replace("#", "%23")
    query = query.replace("&", "%26")
    query = query.replace("=", "%3D")
    query = query.replace(" ", "%20")

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
