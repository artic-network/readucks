#!/usr/bin/env python3
"""
Run 'pip install .' to install Readucks.
"""

# Make sure this is being run with Python 3.4 or later.
import sys
if sys.version_info.major != 3 or sys.version_info.minor < 4:
    print('Error: you must execute setup.py using Python 3.4 or later')
    sys.exit(1)

import os
import shutil
from distutils.command.build import build
from distutils.core import Command
import subprocess
import multiprocessing
import fnmatch
import importlib.util

# Install setuptools if not already present.
if not importlib.util.find_spec("setuptools"):
    import ez_setup
    ez_setup.use_setuptools()

from setuptools import setup
from setuptools.command.install import install

# Get the program version from another file.
exec(open('readucks/version.py').read())

with open('README.md', 'rb') as readme:
    LONG_DESCRIPTION = readme.read().decode()


class Build(build):
    """
    The build process.
    """

    def run(self):
        build.run(self)  # Run original build code


class Install(install):
    """
    The install process.
    """

    def run(self):
        install.run(self)  # Run original install code


class Clean(Command):
    """
    Custom clean command that really cleans up everything, except for:
      - the compiled *.so file needed when running the programs
      - setuptools-*.egg file needed when running this script
    """
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd

        delete_directories = []
        for root, dir_names, filenames in os.walk(self.cwd):
            for dir_name in fnmatch.filter(dir_names, '*.egg-info'):
                delete_directories.append(os.path.join(root, dir_name))
            for dir_name in fnmatch.filter(dir_names, 'build'):
                delete_directories.append(os.path.join(root, dir_name))
            for dir_name in fnmatch.filter(dir_names, '__pycache__'):
                delete_directories.append(os.path.join(root, dir_name))
        for delete_directory in delete_directories:
            print('Deleting directory:', delete_directory)
            shutil.rmtree(delete_directory)

        delete_files = []
        for root, dir_names, filenames in os.walk(self.cwd):
            for filename in fnmatch.filter(filenames, 'setuptools*.zip'):
                delete_files.append(os.path.join(root, filename))
            for filename in fnmatch.filter(filenames, '*.o'):
                delete_files.append(os.path.join(root, filename))
            for filename in fnmatch.filter(filenames, '*.pyc'):
                delete_files.append(os.path.join(root, filename))
        for delete_file in delete_files:
            print('Deleting file:', delete_file)
            os.remove(delete_file)


setup(name='readucks',
      version=__version__,
      description='Readucks: a simple demultiplexer for nanopore reads',
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      url='http://github.com/rambaut/readucks',
      author='Andrew Rambaut',
      author_email='a.rambaut@ed.ac.uk',
      license='GPL',
      packages=['readucks'],
      entry_points={"console_scripts": ['readucks = readucks.readucks:main']},
      zip_safe=False,
      cmdclass={'build': Build,
                'install': Install,
                'clean': Clean}
      )
