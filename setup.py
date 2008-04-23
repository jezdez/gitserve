#!/usr/bin/env python

import os, sys
from setuptools import setup, find_packages
#from gitserve.__init__ import __version__ as VERSION

setup(
    name="gitserve",
    version='0.1.0',
    description="A helper tool for git that mimics mercurial\'s serve command",
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    url='http://github.com/jezdez/git-serve/',
    keywords="PyPI setuptools cheeseshop distutils eggs package management",
    install_requires=["setuptools"],
    packages=find_packages('src'),
    package_dir={'':'src'},
    package_data={'': ['media/*.*', 'cgi-bin/*.cgi'],},
    entry_points={'console_scripts': ['git-serve = gitserve:runserver',]},
    zip_safe=False,
    include_package_data = True,
)

# from pkg_resources import Environment, Requirement, resource_filename, require
# 
# env = Environment()
# git_serve = env["git-serve"][0]
# env.remove(git_serve)
#env.scan()
#require('git-serve')

# gitweb_cgi = resource_filename(
#     Requirement.parse('git-serve'), 'gitserve/cgi-bin/gitweb.cgi')
# 
# print "######", gitweb_cgi
# if not os.access(gitweb_cgi, os.X_OK):
#     os.chmod(gitweb_cgi, 0755)

try:
    import gitserve
except:
    pass
else:
    gitweb_cgi = os.path.join(
        os.path.dirname(os.path.abspath(gitserve.__file__)),
            "cgi-bin", "gitweb.cgi")
    if not os.access(gitweb_cgi, os.X_OK):
        try:
            os.chmod(gitweb_cgi, 0755)
        except OSError:
            pass
        else:
            print "Making gitweb.cgi executable"
