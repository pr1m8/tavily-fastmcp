"""Prompt loading helpers.

Purpose:
    Load packaged markdown prompts by name and list the prompt files shipped
    with the package.

Design:
    - Prompt files live under ``tavily_fastmcp.prompts``.
    - Prompt names are addressed without the ``.md`` suffix.

Examples:
    >>> "router" in list_prompt_names()
    True
    >>> load_prompt_text("router").startswith("#")
    True
"""

from __future__ import annotations

from importlib.resources import files


def list_prompt_names() -> list[str]:
    """Return the packaged prompt names.

    Returns:
        Sorted prompt names without file extensions.

    Raises:
        FileNotFoundError: If the prompts package is unavailable.

    Examples:
        >>> isinstance(list_prompt_names(), list)
        True
    """
    prompt_dir = files("tavily_fastmcp.prompts")
    return sorted(path.stem for path in prompt_dir.iterdir() if path.suffix == ".md")


def load_prompt_text(name: str) -> str:
    """Load a packaged markdown prompt.

    Args:
        name: Prompt name without ``.md``.

    Returns:
        The markdown contents of the prompt file.

    Raises:
        FileNotFoundError: If the prompt does not exist.

    Examples:
        >>> text = load_prompt_text("router")
        >>> text.startswith("# ")
        True
    """
    return files("tavily_fastmcp.prompts").joinpath(f"{name}.md").read_text(encoding="utf-8")
