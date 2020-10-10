#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Niranjan Kiran Kumar Dhurjaty",
    author_email='nidhurja@cisco.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Endpoint Posturing with AMP4E-Orbital",
    install_requires=requirements,
    license="Cisco Sample Code License, Version 1.1",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='posturingaa',
    name='posturingaa',
    packages=find_packages(include=['posturingaa']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kdhurjaty/posturingaa',
    version='0.1.0',
    zip_safe=False,
)
