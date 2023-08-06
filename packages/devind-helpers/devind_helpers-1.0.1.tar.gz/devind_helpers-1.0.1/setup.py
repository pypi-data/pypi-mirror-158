# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devind_helpers',
 'devind_helpers.files',
 'devind_helpers.generators',
 'devind_helpers.import_from_file',
 'devind_helpers.schema']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.2,<5.0.0',
 'flatten-dict>=0.4.2,<0.5.0',
 'graphql-core>=3.2.1,<4.0.0',
 'inflection>=0.5.1,<0.6.0',
 'openpyxl>=3.0.10,<4.0.0',
 'redis>=4.3.4,<5.0.0',
 'strawberry-django-plus>=1.17.0,<2.0.0']

setup_kwargs = {
    'name': 'devind-helpers',
    'version': '1.0.1',
    'description': 'Devind helpers.',
    'long_description': '# Devind helpers python library.',
    'author': 'Victor',
    'author_email': 'lyferov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/devind-django-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
