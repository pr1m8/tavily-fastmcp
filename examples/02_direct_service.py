"""Direct Tavily service example.

Examples:
    >>> callable(main)
    True
"""

from tavily_fastmcp.service import LangChainTavilyService
from tavily_fastmcp.settings import get_settings


def main() -> None:
    """Execute a direct Tavily search."""
    service = LangChainTavilyService(get_settings())
    result = service.search_from_model(query="latest Tavily research docs")
    print(result)


if __name__ == "__main__":
    main()
