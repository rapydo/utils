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

from rapydo.utils import __version__

# BUG https://stackoverflow.com/a/14220893
# from setuptools import setup
from distutils.core import setup

setup(
    name='rapydo_utils',
    description='Do development and deploy with the RAPyDo framework',
    version=__version__,
    author="Paolo D'Onorio De Meo",
    author_email='p.donorio.de.meo@gmail.com',
    url='https://github.com/rapydo/utils',
    license='MIT',
    packages=[
        'rapydo.utils'
    ],
    package_data={
        'rapydo.utils': [
            'logging.ini'
        ]
    },
    python_requires='>=3.4',
    install_requires=[
        # NOTE: install_requires specify what a project
        # minimally needs to run correctly
        "beeprint",
        "PyYAML",
        "pytz",
        # NOTE: Requirements files are often used to define
        # the requirements for a complete python environment.
    ],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    keywords=['utilities', 'rapydo']
    # download_url='https://github.com/author/repo/tarball/1.0',
)
