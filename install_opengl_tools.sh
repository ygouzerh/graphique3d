#! /bin/sh
# Date : 11/03/2018
# Purpose : Automatically uninstall and install opengl_tools package for the user

python3 -m pip uninstall opengl_tools
cd opengl_tools_package
python3 -m pip install --user .
