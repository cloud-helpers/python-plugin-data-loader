#
# File: https://github.com/cloud-helpers/python-plugin-data-loader/blob/main/docs/conf.py
#
# Doc: https://www.sphinx-doc.org/en/master/usage/configuration.html
#

import os
import sys

sys.path.insert(0, os.path.abspath('extensions'))

extensions = ['sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinx.ext.coverage', 'sphinx.ext.ifconfig']

todo_include_todos = True
templates_path = ['_templates']
source_suffix = '.html'
master_doc = 'index'
exclude_patterns = []
add_function_parentheses = True
#add_module_names = True
# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

project = u'Python plugin/extra to load data files from an external source (such as AWS S3) to a local directory'
copyright = u'2020-2026, Denis Arnaud'

version = ''
release = ''

# -- Options for HTML output ---------------------------------------------------

html_theme = 'alabaster'
html_theme_path = ['themes']
html_title = "Python plugin/extra to load data files from an external source (such as AWS S3) to a local directory"
#html_short_title = None
#html_logo = None
#html_favicon = None
html_static_path = ['_static']
html_domain_indices = False
html_use_index = False
html_show_sphinx = False
htmlhelp_basename = 'DataLoaderPlugindoc'
html_show_sourcelink = False


################################################################################


def setup(app):
     from sphinx.util.texescape import tex_replacements
     tex_replacements += [(u'♮', u'$\\natural$'),
                          (u'ē', u'\=e'),
                          (u'♩', u'\quarternote'),
                          (u'↑', u'$\\uparrow$'),
                          ]

