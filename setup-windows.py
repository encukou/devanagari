#! /usr/bin/python

from distutils.core import setup
import py2exe

from setup import setup_params

import psyco
psyco.full()

setup_params['zipfile']="library.p2e";
setup_params['windows']=[{
                'script': "(set later)", 
                'target': "devanagari.exe",
                #"icon_resources": [(1, r"icon.ico")],
              }]
setup_params['options']={
                "py2exe":{
                        "includes": ["sip","SendKeys","sys"],
                        "excludes": ["Tkconstants","Tkinter","tcl"],
                        "compressed": 0,
                        "optimize": 2,
                }
        }


#setup_params["windows"][0]["script"]="to-devanagari.py"; setup(**setup_params)

setup_params["windows"][0]["script"]="gui.py"; setup(**setup_params)

