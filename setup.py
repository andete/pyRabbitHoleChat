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
      'packages':'encodings',
      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
      'includes': 'cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms, rsvg',
  }
  extra_data_files = ['msvcp90.dll',]
  extra_options = dict(
      setup_requires=['py2exe'],
      console=['pyRabbitHoleChat.py'],
      options=dict(py2exe=OPTIONS)
      )
  # Find GTK+ installation path
  __import__('gtk')
  m = sys.modules['gtk']
  gtk_base_path = m.__path__[0]

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
