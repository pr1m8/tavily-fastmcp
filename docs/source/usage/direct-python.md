# Direct Python

```python
from tavily_fastmcp.service import LangChainTavilyService
from tavily_fastmcp.settings import get_settings

service = LangChainTavilyService(get_settings())
result = service.search_from_model(query="FastMCP prompts docs")
```
