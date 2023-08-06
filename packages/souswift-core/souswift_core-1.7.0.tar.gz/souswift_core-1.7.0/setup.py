# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['souswift_core',
 'souswift_core.exc',
 'souswift_core.filters',
 'souswift_core.providers',
 'souswift_core.providers.database',
 'souswift_core.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.29,<2.0.0',
 'aiomysql>=0.0.22,<0.0.23',
 'context-handler>=4.0.0,<5.0.0',
 'fastapi>=0.71.0,<0.72.0',
 'orjson>=3.6.6,<4.0.0',
 'pydantic[email]>=1.9.0,<2.0.0',
 'tzdata>=2021.5,<2022.0']

setup_kwargs = {
    'name': 'souswift-core',
    'version': '1.7.0',
    'description': '',
    'long_description': None,
    'author': 'Gustavo Correa',
    'author_email': 'self.gustavocorrea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
