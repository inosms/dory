#!/usr/bin/env python

from setuptools import setup
import sys

if sys.version_info[0] < 3:
    print("python < 3.0 is not supported :(")
    sys.exit(0)

setup(name='Dory',
      version='0.0.6',
      description='Simple Backup',
      author='inosms',
      url='https://github.com/inosms/dory',
      packages=["dory"],
      entry_points={
      "console_scripts":["dory=dory.dory:main"]
      },
      install_requires = ["termcolor"]
     )
