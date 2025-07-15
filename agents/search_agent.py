
from langchain.tools import tool
from langchain_community.tools.brave_search.tool import BraveSearch

search = BraveSearch.from_env()

@tool("search_internet", return_direct=True)
def search_internet(query: str) -> list:
    """
    Search the internet using Brave Search and return top 3 results.
    Args:
        query: The search query string.
    Returns:
        List of dicts with 'title', 'url', and 'snippet'.
    """
    results = search.run(query)
    # If results is a string, try to parse as JSON
    import json
    try:
        results = json.loads(results)
    except Exception:
        pass
    if isinstance(results, list):
        return results[:3]
    return results
