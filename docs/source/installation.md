# Installation

Install the published package:

```bash
pdm add tavily-fastmcp
```

For LangChain helpers:

```bash
pdm add "tavily-fastmcp[langchain]"
```

For repository development, install all groups:

```bash
pdm install -G:all
```

or:

```bash
make install
```

Create local credentials only when you need live Tavily calls:

```bash
cp .env.example .env
# edit .env and set TAVILY_API_KEY
```
