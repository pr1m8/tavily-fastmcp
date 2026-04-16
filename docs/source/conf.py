"""Sphinx configuration for tavily-fastmcp docs."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

project = "tavily-fastmcp"
author = "William R. Astley"
release = "0.3.0"

extensions = [
    "myst_parser",
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinx_inline_tabs",
    "sphinxcontrib.mermaid",
    "sphinx_autodoc_typehints",
    "autodoc_pydantic",
    "autoapi.extension",
    "sphinxext.opengraph",
    "sphinx_sitemap",
    "notfound.extension",
    "sphinx_last_updated_by_git",
    "sphinx_reredirects",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "https://tavily-fastmcp.readthedocs.io/")

autoapi_type = "python"
autoapi_dirs = [str(SRC / "tavily_fastmcp")]
autoapi_add_toctree_entry = False
autoapi_keep_files = True

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "substitution",
    "tasklist",
]
