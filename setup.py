# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='histograph',
    version='0.1.0',
    description='Histograph API Client library',
    long_description='Histograph API Python bindings',
    author='Roman Kalyakin',
    author_email='roman@kalyakin.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests'))
)
