__author__ = 'James Stidard'

from setuptools import setup, find_packages

version = '0.1'

setup(name='utilise-py',
      version=version,
      packages=find_packages(exclude=['tests*']),
      include_package_data=True,
      install_requires=['setuptools'])

setup(name='utilise-py',
      version=version,
      packages=['utilise'],
      package_dir={'utilise': 'src/utilise'},
      include_package_data=True,
      exclude_package_data={'': ['*tests/*']},
      install_requires=['setuptools'])
