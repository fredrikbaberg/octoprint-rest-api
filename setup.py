#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'asyncio']

extras_requirements={'test': ['pytest', 'pytest-xdist', 'tox']}

setup(
    author="Fredrik Baberg",
    author_email='fredrik.baberg@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="OctoPrint REST API for communicating with OctoPrint instance",
    entry_points={
        'console_scripts': [
            'octoprint_rest_api=octoprint_rest_api.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='octoprint_rest_api',
    name='octoprint-rest-api-fredrikbaberg',
    packages=find_packages(include=['octoprint_rest_api']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    extras_require=extras_requirements,
    url='https://github.com/fredrikbaberg/octoprint_rest_api',
    version='0.0.6',
    zip_safe=False,
)
