# -*- coding: utf-8 -*-

from utilities import __version__
from utilities import DEFAULT_FILENAME
from setuptools import setup

setup(
    name='rapydo-utils',
    description='A set of python utilities used across all RAPyDo projects',
    version=__version__,
    author="Paolo D'Onorio De Meo",
    author_email='p.donorio.de.meo@gmail.com',
    url='https://github.com/rapydo/utils',
    license='MIT',
    packages=[
        # NOTE to self: it was not a good idea to share the package prefix
        'utilities'
    ],
    package_data={
        'utilities':
        [
            'logging.ini',
            '%s.yaml' % DEFAULT_FILENAME
        ]
    },
    python_requires='>=3.4',
    install_requires=[
        # NOTE: install_requires specify what a project
        # minimally needs to run correctly
        "beeprint",
        "PyYAML",
        "pytz",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    keywords=['utilities', 'rapydo', 'logs', 'tools']
)
