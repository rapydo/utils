# -*- coding: utf-8 -*-

"""
RAPyDo utils
-----

Welcome to our new RAPyDo framework.

Utilities
````````````

This is just a set of python utilities used
across all rapydo projects.

Links
`````
* `github <http://github.com/rapydo>`_
"""

from setuptools import setup
# from distutils.core import setup
from rapydo.utils import __version__

setup(
    name='rapydo_utils',
    description='Do development and deploy with the RAPyDo framework',
    version=__version__,
    author="Paolo D'Onorio De Meo",
    author_email='p.donorio.de.meo@gmail.com',
    url='https://github.com/rapydo/utils',
    license='MIT',
    packages=[
        # 'rapydo',
        'rapydo.utils'
    ],
    package_data={
        'rapydo.utils': [
            'logging.ini'
        ]
    },
    python_requires='>=3.4',
    # entry_points={
    #     'console_scripts': [
    #         'rapydo=rapydo.do.__main__:main',
    #     ],
    # },
    install_requires=[
        "beeprint",
        # "better_exceptions",
        "pytz"
    ],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    keywords=['utilities', 'rapydo']
    # download_url='https://github.com/author/repo/tarball/1.0',
)
