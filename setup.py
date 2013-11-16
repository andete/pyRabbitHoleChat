#! /usr/bin/env python2

import glob, sys, platform
from setuptools import setup

VERSION='0.1'

with open('README.md') as file:
    long_description = file.read()

extra_options = {}

if sys.platform == 'win32':
  import py2exe
  OPTIONS = {
  }
  extra_data_files = ['msvcp90.dll',]
  extra_options = dict(
      setup_requires=['py2exe'],
      console=['pyRabbitHoleChat.py'],
      options=dict(py2exe=OPTIONS)
      )
elif sys.platform.startswith('linux'):
  extra_options = dict(
      # Normally unix-like platforms will use "setup.py install"
      # and install the main script as such
      scripts=['pyRabbitHoleChat.py'],
      )

elif sys.platform == 'darwin':
  raise Exception("TODO OS-X app.")
else:
  raise Exception("unknown platform: " + sys.platform)

setup(
  name = 'pyRabbitHoleChat',
  description = 'Chat client for the Rabbit Hole hackerspace',
  long_description = long_description,
  author = 'Paul "Vi" Schimmelpfenning',
  author_email = 'paul@pjschim.com',
  version = VERSION,
  url = 'https://github.com/pjschim/pyRabbitHoleChat',
  packages = [],
  #packages_data = { '': ['config','GUI.xml'] },
  data_files = [('share/pyRabbitHoleChat', ['GUI.xml', 'config'])],
  platforms = ["Windows", "Linux", "Mac OS-X"],
  **extra_options
  )
