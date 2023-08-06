# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katzcom']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0', 'python-osc>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'katzcom',
    'version': '0.2.0',
    'description': 'Katz domain communications.',
    'long_description': None,
    'author': 'Kevin Katz',
    'author_email': 'contact@kevinkatz.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
