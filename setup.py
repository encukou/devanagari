#!/usr/bin/env python

# This doesn't really work, anybody want to fix it?

# (My users are all windows-based, so it's not worth it for me to support
#  regular Python installation. I just run ./gui.py and all's right.)

from distutils.core import setup

from version import version

setup_params={
  'name':'Devanagari',
  'version':version,
  'description':'Devanagari Converter',
  'author':'Petr Viktorin',
  'author_email':'encukou@gmail.com',
  #'url':'http://?',
  'packages':[''],
  'license': "GPLv3",
}

if __name__=="__main__":
  setup(**setup_params)
