# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages

setup(
    name='straceviewer',
    version='1.0',
    description='Parser/Viewer for strace output',
    author='Jérôme Perrin',
    packages=find_packages('.'),
    test_suite="tests",
    install_requires=["lark-parser"]
)
