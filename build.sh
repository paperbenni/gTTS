#!/usr/bin/env bash
rm -rf dist/*
python3 setup.py sdist bdist_wheel

rm -rf ~/.local/lib/python3.7/site-packages/cursetup*
cd dist
pip3 install --user ./g*.whl
