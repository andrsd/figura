import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'figura'
copyright = '2022-2023, David Andrs'
author = 'David Andrs'

master_doc = 'index'
templates_path = ['_templates']

exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = []
html_show_sourcelink = False

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_design'
]

autoclass_content = "init"
autodoc_default_options = {
    'undoc-members': True
}
