#!/usr/bin/env python

import os, sys
from setuptools import setup, find_packages
from gitserve.__init__ import __version__ as VERSION

setup(
    name='gitserve',
    version=VERSION,
    description="A helper tool for git that mimics mercurial\'s serve command",
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    url='http://github.com/jezdez/git-serve/',
    keywords="PyPI setuptools cheeseshop distutils eggs package management",
    install_requires=["setuptools"],
    packages=find_packages('src'),
    package_dir={'':'src'},
    package_data={'': ['media/*.*', '*.cgi', '*.conf'],},
    entry_points={'console_scripts': ['git-serve = gitserve:main',]},
    zip_safe=False,
    include_package_data = True,
)

try:
    import gitserve
except:
    pass
else:
    gitweb_cgi = os.path.join(
        os.path.dirname(os.path.abspath(gitserve.__file__)), "gitweb.cgi")
    if not os.access(gitweb_cgi, os.X_OK):
        try:
            os.chmod(gitweb_cgi, 0755)
        except OSError:
            pass
        else:
            print "Making gitweb.cgi executable"
