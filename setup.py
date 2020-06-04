import setuptools

setuptools.setup(
    name='GraphPipe',
    version='1.0',
    packages=setuptools.find_packages(),
    url='https://github.com/gabecarra/GraphPipe',
    license='MIT',
    author='Gabriel Henrique Carraretto',
    author_email='carrag@usi.ch',
    description='The following project consists in a python package that applies 2D multi-person pose estimation to images and videos, and parses the results into attributed graphs. The goal of this project is to make available an all-in-one tool to build datasets based on real time 2D multi-person detection, and is part of my bachelor project at USI.'
)
