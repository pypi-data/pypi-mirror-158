#!/usr/bin/bash

name=smgantt

rm -rf build/ dist/ $name.egg-info/

python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*

pip uninstall $name -y
pip install $name -U -i https://pypi.org/simple
