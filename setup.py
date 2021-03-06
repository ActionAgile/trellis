#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements_lines = [line.strip() for line in open('requirements.txt')
                      .readlines()]
install_requires = list(filter(None, requirements_lines))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.md').read().replace('.. :changelog:', '')

setup(
    name='trellostats',
    version=0.4,
    description='Trello stats for winners.',
    long_description=readme + '\n\n' + history,
    author='Ben Hughes',
    author_email='bwghughes@gmail.com',
    url='https://github.com/actionagile/trellis',
    include_package_data=True,
    install_requires=install_requires,
    license="BSD",
    zip_safe=False,
    keywords=['trello', 'cycle_time'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts':
        ['trellostats=cli:cli']
    }

)
