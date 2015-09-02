__author__ = 'James Stidard'

from setuptools import setup

version = '0.2.0'

setup(name='utilise-py',
      version=version,
      packages=['utilise'],
      package_dir={'utilise': 'src/utilise'},
      include_package_data=True,
      exclude_package_data={'': ['*tests/*']},
      install_requires=['setuptools'])
