# -*- coding: utf-8 -*-

from setuptools import setup
from utilities import \
    __version__, __package__ as main_package, DEFAULT_FILENAME

setup(
    name='rapydo-utils',
    version=__version__,
    description='A set of python utilities used across all RAPyDo projects',
    author="Paolo D'Onorio De Meo",
    author_email='p.donorio.de.meo@gmail.com',
    url='https://rapydo.github.io/utils/',
    license='MIT',
    packages=[main_package],
    package_data={
        main_package: [
            'logging.ini',
            '%s.yaml' % DEFAULT_FILENAME
        ]
    },
    python_requires='>=3.4',
    install_requires=[
        "beeprint",
        "PyYAML",
        "pytz",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['utilities', 'rapydo', 'logs', 'tools']
)
