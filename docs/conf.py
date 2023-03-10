import os
import sys

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
rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
"""
