import os, sys 

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../"))

project = "wyvern"
copyright = "2023, sarthhh"
author = "sarthhh"
release = "0.2.0"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.napoleon", "myst_parser"]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
html_theme = "furo"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
autodoc_inherit_docstrings = True
html_css_files = [
    "style.css",
]

html_static_path = ["_static"]
