#!/usr/bin/env python

import os, sys, stat
from setuptools import setup, find_packages

setup(
    name='gitserve',
    version='0.1.1',
    license='GPL2',
    description="A helper tool for git that mimics mercurial\'s serve command",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    url='http://github.com/jezdez/git-serve/',
    keywords="git dvcs mercurial serve cgi",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Version Control',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
    install_requires=["setuptools"],
    packages=find_packages('src'),
    package_dir={'':'src'},
    package_data={'': ['media/*.*', '*.so', '*.conf'],},
    entry_points={'console_scripts': ['git-serve = gitserve:main',],},
    zip_safe=False,
    include_package_data = True,
)
