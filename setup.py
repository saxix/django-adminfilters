#!/usr/bin/env python
import codecs
import imp
import os
import sys

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'adminfilters', '__init__.py')

app = imp.load_source('adminfilters', init)
reqs = 'install.py%d.pip' % sys.version_info[0]


def read(*files):
    content = ''
    for f in files:
        content += codecs.open(os.path.join(ROOT, 'src',
                                            'requirements', f), 'r').read()
    return content

install_requires = read('install.any.pip', reqs)
tests_requires = read('testing.pip')
dev_requires = tests_requires + read('develop.pip')


setup(name=app.NAME,
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
          'test': tests_requires,
          'dev': dev_requires
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
      long_description=codecs.open('README.rst').read()
      )
