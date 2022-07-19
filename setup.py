#!/usr/bin/env python3
#
#

import os
from setuptools import setup

required=[]
with open('requirements.txt') as f:
    for line in f.read().splitlines():
        if line.strip() and "#" not in line:
            required.append(line)

setup(
    name='svg2dxf',
    version='0.1.0',
    author='Oliver Dippel',
    author_email='o.dippel@gmx.de',
    packages=['svg2dxf'],
    scripts=['bin/svg2dxf'],
    url='http://pypi.python.org/pypi/svg2dxf/',
    license='LICENSE',
    description='python based svg to dxf converter',
    long_description=open('README.md').read(),
    install_requires=required,
    include_package_data=True,
    data_files = [ ('data', []) ]
)

