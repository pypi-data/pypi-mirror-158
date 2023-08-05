#!/usr/bin/python3
# Setup script to install this package.
# M.Blakeney, Mar 2018.

from pathlib import Path
from setuptools import setup

name = 'docker-machine-add-ssh'
module = name.replace('-', '_')
here = Path(__file__).resolve().parent

setup(
    name=name,
    version='1.6',
    description='Adds docker-machine ssh configuration into your '
    'personal ssh configuration',
    long_description=here.joinpath('README.md').read_text(),
    long_description_content_type="text/markdown",
    url='https://github.com/bulletmark/{}'.format(name),
    author='Mark Blakeney',
    author_email='mark.blakeney@bullet-systems.net',
    keywords=['docker', 'docker-machine', 'ssh'],
    license='GPLv3',
    py_modules=[module],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    data_files=[
        ('share/{}'.format(name), ['README.md']),
    ],
    entry_points={
        'console_scripts': ['{}={}:main'.format(name, module)],
    },
)
