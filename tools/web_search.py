"""Web search tool for the research agent."""
import requests
from bs4 import BeautifulSoup
from typing import Optional


def web_search_tool(query: str, num_results: int = 3) -> dict:
    """Search the web for information on a given topic.

    This tool performs a web search and returns relevant snippets
    from top results. Useful for gathering current information,
    facts, and data points on any topic.

    Args:
        query: The search query string.
        num_results: Number of results to return (default: 3).

    Returns:
        dict: A dictionary containing search results with titles,
              snippets, and URLs.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; ResearchAgent/1.0)"
        }

        # Use DuckDuckGo HTML search as a lightweight search
        url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"Search failed with status {response.status_code}",
                "results": []
            }

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.select(".result")[:num_results]:
            title_elem = result.select_one(".result__title")
            snippet_elem = result.select_one(".result__snippet")
            link_elem = result.select_one(".result__url")

            title = title_elem.get_text(strip=True) if title_elem else "No title"
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else "No snippet"
            link = link_elem.get_text(strip=True) if link_elem else "No URL"

            results.append({
                "title": title,
                "snippet": snippet,
                "url": link,
            })

        return {
            "status": "success",
            "query": query,
            "num_results": len(results),
            "results": results,
        }

    except requests.Timeout:
        return {
            "status": "error",
            "message": "Search request timed out",
            "results": []
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Search failed: {str(e)}",
            "results": []
        }
