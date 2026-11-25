"""Sphinx configuration for the Sticky Notes documentation."""
import os
import sys

import django

# Make the Django project importable and configure Django so that
# autodoc can import the models, forms and views.
sys.path.insert(0, os.path.abspath(os.path.join("..", "sticky_notes")))
os.environ["DJANGO_SETTINGS_MODULE"] = "sticky_notes.settings"
django.setup()

# -- Project information -----------------------------------------------------

project = "Sticky Notes"
copyright = "2026, Joshua"
author = "Joshua"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
