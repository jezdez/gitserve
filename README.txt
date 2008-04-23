=========
git-serve
=========

This is a helper tool for git that mimics mercurial_'s serve_ command.

It makes it very easy to see all your git project via git_'s own gitweb_ by
running a lightweight local server.

.. _mercurial: http://www.selenic.com/mercurial/
.. _serve: http://www.selenic.com/mercurial/wiki/index.cgi/hgserve
.. _git: http://git.or.cz/
.. _gitweb: http://git.or.cz/gitwiki/Gitweb

Usage
-----

When ``git-serve`` was installed correctly (with ``sudo``) it's usually located in
``/usr/local/bin``. Note that this directory needs to be on your ``$PATH``
environment variable to be found by your shell.

Usage pretty easy::

    $ git-serve --help
    Usage: git-serve [options] <dir>

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -v, --verbose         print status messages to stdout
      -q, --quiet           don't print anything to stdout
      -p PORT, --port=PORT  port to listen on (default: 8000)
      -a ADDRESS, --address=ADDRESS
                            address to listen on (default: all interfaces)
      -b, --browser         open default browser automatically
      -d, --daemon          detach from terminal and become a daemon
      --pid-file=PIDFILE    write the spawned process-id to this file

As the only argument you can specify a directory that contains your git
projects. If you leave this argument blank ``git-serve`` will automatically uses
the current directory as the source for the gitweb script. E.g.::

    $ git-serve /home/jannis/git-projects

Shortcuts in the directory argument are also possible and will be expanded on
runtime::

    $ git-serve ~/git-projects

The default ``git-serve`` process will listen on your machine's hostname and on
port 8000, for example: http://127.0.0.1:8000/

If you provide a ``--port`` or ``--address`` option while starting ``git-serve``
you can have ``git-serve`` listen on your choices. You need to be root to run it
on port 80 or any other port below 1024.

The ``--browser`` option tells ``git-serve`` to automatically start your system's
default web browser with the URL of the ``git-serve`` server while starting it.

The ``--daemon`` option causes the whole ``git-serve`` process to detach from your
current shell session, becoming a daemon process that runs in background. This
is very useful in combination with the ``--pid-file`` option that write the
process id in the given file.

