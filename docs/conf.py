"""Configuration file for the Sphinx documentation builder."""

# Reference: http://www.sphinx-doc.org/en/master/config

import os
import sys

# Add module directory to sys.path for autodoc to import the module.
sys.path.insert(0, os.path.abspath('..'))

# To prevent isort, pycodestyle, and pylint errors, the import statement
# is placed within try-except block.
try:
    import myhn
except ImportError as e:
    print('{}: {}'.format(type(e).__name__, str(e)), file=sys.stderr)
    sys.exit(1)

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

# Let Read the Docs choose its default theme.
# html_theme = 'alabaster'

# Paths that contain custom static files, relative to this directory.
html_static_path = ['_static']

# To support Sphinx 1.8.5 installed in Travis CI Python 3.4 environment.
master_doc = 'index'

# Version information.
version = myhn.__version__.split('.')[2]
release = myhn.__version__
