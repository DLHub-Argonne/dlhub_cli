import os
from setuptools import setup, find_packages

# single source of truth for package version
version_ns = {}
with open(os.path.join("dlhub_cli", "version.py")) as f:
    exec(f.read(), version_ns)
version = version_ns['__version__']

setup(
    name="dlhub-cli",
    version=version,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'click>=6.6,<7.0',
        'requests>=2.0.0,<3.0.0'
    ],

    entry_points={
        'console_scripts': ['dlhub = dlhub_cli:cli_root']
    },

    # descriptive info, non-critical
    description="DLHub CLI",
    long_description=open("README.md").read(),
    author="Ryan Chard",
    author_email="rchard@anl.gov",
    url="https://github.com/DLHub-Argonne/dlhub-cli",
    keywords=["dlhub", "cli", "command line"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
)