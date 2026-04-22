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
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinx_inline_tabs",
    "sphinxcontrib.mermaid",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
    "autoapi.extension",
    "sphinxext.opengraph",
    "notfound.extension",
    "sphinx_last_updated_by_git",
    "sphinx_reredirects",
]

if os.environ.get("READTHEDOCS") == "True":
    extensions.append("sphinx_sitemap")

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
autoapi_keep_files = False

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "substitution",
    "tasklist",
]
