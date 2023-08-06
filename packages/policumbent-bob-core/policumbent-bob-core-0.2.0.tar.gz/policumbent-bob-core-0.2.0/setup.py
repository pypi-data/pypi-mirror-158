# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['core']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'paho-mqtt>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'policumbent-bob-core',
    'version': '0.2.0',
    'description': 'BOB common files',
    'long_description': None,
    'author': 'Gabriele Belluardo',
    'author_email': 'gabriele.belluardo@outlook.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
