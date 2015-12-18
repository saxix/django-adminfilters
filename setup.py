#!/usr/bin/env python
from __future__ import absolute_import

import os
import sys
import codecs

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(ROOT, 'src'))

app = __import__('adminfilters')
NAME = app.NAME
RELEASE = app.get_version()


def read(*path):
    return codecs.open(os.path.join(ROOT, *path)).read()

tests_require = read('requirements', 'testing.pip')
dev_require = read('requirements', 'develop.pip')

setup(
    name=app.NAME,
    version=app.get_version(),
    url='https://github.com/saxix/django-adminfilters',
    download_url='https://github.com/saxix/django-adminfilters',
    author='sax',
    author_email='sax@os4d.org',
    description="Extra filters for django admin site",
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    # install_requires=fread(reqs),
    # tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'dev': dev_require + tests_require,
    },
    platforms=['any'],
    command_options={
        'build_sphinx': {
            'version': ('setup.py', app.VERSION),
            'release': ('setup.py', app.VERSION)}
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers'],
    long_description=read('README.rst')
)
