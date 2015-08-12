__author__ = 'James Stidard'

from setuptools import setup, find_packages

version = '0.1'

setup(name='utilise-py',
      version=version,
      packages=find_packages('src', exclude=['src.tests*']),
      include_package_data=True,
      exclude_package_data = {'': ['*tests/*']},
      install_requires=['setuptools'])
