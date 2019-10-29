# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from setuptools import setup, find_packages

setup(
    name='dia_util',
    version='0.1',
    packages=find_packages(exclude=["*.examples"]),
    install_requires=[
        'Django==2.1', 'PyMySQL==0.8.0'],
    license='Hermogenes Batista All rights reserved',
    long_description='Hermogenes Batista All rights reserved',
)

