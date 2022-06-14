import setuptools

long_desc = open("README.md").read()
required = [csv, math, os, time, queue, shlex, subprocess, threading, cv2, re, requests, shutil, olympe] # Comma seperated dependent libraries name

setuptools.setup(
    name="ParrotController",
    version="1.0.0",
    author="Kevyn Angueira Irizarry",
    author_email="kevyn.angueira@gmail.com",
    license="liscence.txt",
    description="Wrapper for Parrot Olympe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boredbot2/Parrot-Controller",
    packages = ['ParrotController'],
    key_words="Parrot Anafi, Drone",
    install_requires=required,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
