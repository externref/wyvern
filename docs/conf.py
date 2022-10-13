import os
import sys

sys.path.insert(0, os.path.abspath(".")) 
sys.path.insert(0, os.path.abspath("..")) 
sys.path.insert(0, os.path.abspath("../"))

project = "wyvern"
copyright = "2022, sarthhh & FallenDeity"
author = "sarthhh, FallenDeity"
release = __import__("wyvern").__version__

extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "furo"
html_static_path = ["_static"]
source_suffix = [".rst", ".md"]
