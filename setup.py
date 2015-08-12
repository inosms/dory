#!/usr/bin/env python

from setuptools import setup

setup(name='Dory',
      version='0.0.1',
      description='Simple Backup',
      author='inosms',
      url='https://github.com/inosms/dory',
      packages=["dory"],
      entry_points={
      "console_scripts":["dory=dory.dory:main"]
      },
      install_requires = ["termcolor"]
     )
