"""Configuration file for the Sphinx documentation builder."""

# Reference: http://www.sphinx-doc.org/en/master/config

import os
import sys

# Add module directory to sys.path for autodoc to import the module.
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'MyHN'
copyright = '2019, Sunaina Pai'
author = 'Sunaina Pai'

# To process `automodule` directive in `.rst` files.
extensions = [
    'sphinx.ext.autodoc',
]

# Paths that contain templates, relative to this directory.
templates_path = ['_templates']

# Exclude patterns relatve to source directory.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The theme to use for HTML and HTML Help pages.
html_theme = 'alabaster'

# Paths that contain custom static files, relative to this directory.
html_static_path = ['_static']
