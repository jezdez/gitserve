#!/usr/bin/env python

import os, sys
try:
    from setuptools import find_packages, setup
    from setuptools.command.easy_install import easy_install
except ImportError:
    sys.exit("Please install a recent version of setuptools")

easy_install.real_process_distribution = easy_install.process_distribution
def process_distribution(self, *args, **kwargs):
    """Brutally ugly hack to have post_install functionality. oh. my. god."""
    easy_install.real_process_distribution(self, *args, **kwargs)

    import pkg_resources
    try:
        pkg_resources.require("gitserve")
        gitweb_cgi = pkg_resources.resource_filename("gitserve", "gitweb.cgi")
        os.chmod(gitweb_cgi, 0755)
    except:
        print "Chmodding failed. Try 'chmod +x /path/to/gitserve/gitweb.cgi'"
easy_install.process_distribution = process_distribution

setup(
    name='gitserve',
    version='0.2.0',
    license='GPL-2',
    description="A helper tool for git that mimics mercurial\'s serve command",
    long_description=open('README.txt', 'r').read(),
    maintainer='Jannis Leidel',
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
    packages=find_packages('src'),
    package_dir={'':'src'},
    package_data={'': ['media/*.*', '*.cgi', '*.conf'],},
    entry_points={'console_scripts': ['gitserve = gitserve:main',],},
    zip_safe=False,
    include_package_data = True,
)
