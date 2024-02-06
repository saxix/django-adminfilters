#!/usr/bin/env python
import ast
import codecs
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'adminfilters', '__init__.py')

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(content).group(1)))
    name = str(ast.literal_eval(_name_re.search(content).group(1)))


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, 'src', 'requirements', *parts), 'r').read()


install_requires = read('install.pip')
tests_requires = read('testing.pip')
dev_requires = tests_requires + read('develop.pip')

setup(
    name=name,
    version=version,
    url='https://github.com/saxix/django-adminfilters',
    download_url='https://github.com/saxix/django-adminfilters',
    author='sax',
    author_email='s.apostolico@gmail.com',
    description='Extra filters for django admin site',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    extras_require={'test': tests_requires, 'dev': dev_requires},
    platforms=['any'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 5.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Developers',
    ],
    long_description=codecs.open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
)
