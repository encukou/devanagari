#! /usr/bin/python

from distutils.core import setup
import py2exe
import os

from setup import setup_params

dllList = ('msvcp90.dll')

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
       if os.path.basename(pathname).lower() in dllList:
               return 0
       return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL


setup_params['zipfile']="library.p2e";
setup_params['windows']=[{
                'script': "(set later)", 
                'target': "devanagari.exe",
                #"icon_resources": [(1, r"icon.ico")],
              }]
setup_params['options']={
                "py2exe":{
                        "includes": ["sip","sys"],
                        "excludes": ["Tkconstants","Tkinter","tcl"],
                        "compressed": 0,
                        "optimize": 2,
                }
        }


#setup_params["windows"][0]["script"]="to-devanagari.py"; setup(**setup_params)

setup_params["windows"][0]["script"]="gui.py"; setup(**setup_params)

