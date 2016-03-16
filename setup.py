#!/usr/bin/env python
from setuptools import setup, find_packages

setup(version='0.1',
      description='BBB Votes 3000',
      author='Mauro Murari',
      author_email='mauro_murari@hotmail.com',
      packages=find_packages(),
      install_requires=['flask', 'pymongo', 'python-decouple'],
      test_suite="restAPI.tests",
)