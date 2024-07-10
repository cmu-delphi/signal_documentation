# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

project = 'Signal Documentation'
copyright = '2023, cmu.edu'
author = 'cmu.edu'
release = '1.0.0'

sys.path.insert(0, os.path.abspath("../.."))

django_settings = "signal_documentation.settings"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinxcontrib_django",
    'sphinx.ext.autodoc',
]

templates_path: list[str] = ['_templates']
exclude_patterns: list = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path: list[str] = ['_static']
