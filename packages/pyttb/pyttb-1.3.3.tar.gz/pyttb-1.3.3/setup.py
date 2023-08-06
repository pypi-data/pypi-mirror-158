# Copyright 2022 National Technology & Engineering Solutions of Sandia,
# LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the
# U.S. Government retains certain rights in this software.

from setuptools import setup

setup(
    name='pyttb',
    version='1.3.3',
    packages=['pyttb'],
    package_dir={'': '.'},
    url='',
    license='',
    author='Danny Dunlavy, Nick Johnson',
    author_email='',
    description='Python Tensor Toolbox (pyttb)',
    install_requires=[
        "numpy",
        "pytest",
        "sphinx_rtd_theme",
        "numpy_groupies"
    ]
)
