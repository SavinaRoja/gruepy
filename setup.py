#/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

def long_desc():
    readme = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme, 'r') as inpt:
        readme_text = inpt.read()
    return readme_text

setup(name='gruepy',
      version='0.0.1',
      long_description=long_desc(),
      author='Paul Barton',
      author_email='pablo.barton@gmail.com',
      url='https://github.com/SavinaRoja/gruepy',
      install_requires=['wcwidth>=1.0.4',],
      packages=['gruepy',],
      license='http://www.gnu.org/licenses/gpl-3.0.html',
      keywords='gruepy, curses, ncurses, terminal, console, UI, asynchronous',
      )

