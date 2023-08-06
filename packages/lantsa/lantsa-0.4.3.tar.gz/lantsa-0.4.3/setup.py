# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lantsa']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.7.5',
 'h5py>=2.9.0',
 'numba>=0.41.0',
 'numpy>=1.17.0',
 'pandas>=1.0',
 'scikit-learn>=0.21.2',
 'torch>=1.7.0',
 'tqdm>=4.56.0']

extras_require = \
{'docs': ['nbsphinx',
          'pydata-sphinx-theme>=0.4.3',
          'scanpydoc>=0.5',
          'sphinx>=3.4',
          'sphinx-autodoc-typehints',
          'sphinx_copybutton<=0.3.1'],
 'docs:python_version >= "3.7"': ['ipython>=7.20'],
 'tutorials': ['leidenalg',
               'python-igraph',
               'scanpy>=1.6',
               'scikit-misc>=0.1.3']}

setup_kwargs = {
    'name': 'lantsa',
    'version': '0.4.3',
    'description': 'Landmark-based transferable subspace analysis for single-cell and spatial transcriptomics',
    'long_description': '# LANTSA\n\nLANTSA is a landmark-based transferable subspace analysis tool for single-cell and spatial transcriptomics.\n\nPlease visit [LANTSA documentation website](https://lantsa.readthedocs.io/) for details about installation, tutorials, API and references.\n',
    'author': 'Lequn Wang',
    'author_email': 'wanglequn2019@sibcb.ac.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
