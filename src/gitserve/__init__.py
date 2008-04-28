#!/usr/bin/python
# encoding: utf-8

__version__ = '0.2.0'

import os
import sys
import posixpath
import webbrowser
from urllib import unquote
from urlparse import urljoin
from optparse import OptionParser
from BaseHTTPServer import HTTPServer
from pkg_resources import resource_filename
from CGIHTTPServer import CGIHTTPRequestHandler
from socket import error as SocketError
from socket import gethostname, gethostbyaddr

def become_daemon(home='.', out_log='/dev/null', err_log='/dev/null'):
    "Robustly turn into a UNIX daemon, running in our_home_dir."
    # First fork
    try:
        if os.fork() > 0:
            sys.exit(0)     # kill off parent
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    os.setsid()
    os.chdir(home)
    os.umask(0)

    # Second fork
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        os._exit(1)

    si = open('/dev/null', 'r')
    so = open(out_log, 'a+', 0)
    se = open(err_log, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    # Set custom file descriptors so that they get proper buffering.
    sys.stdout, sys.stderr = so, se

class GitWebRequestHandler(CGIHTTPRequestHandler):
    cgi_directories = []
    gitserve_media = resource_filename("gitserve", "media")
    aliases = [('/media', gitserve_media),]
    verbose = False
    
    def log_message(self, format, *args):
        if self.verbose:
            CGIHTTPRequestHandler.log_message(self, format, *args)

    def send_error(self, code, message=None):
        if code == 404 and self.path in ('/', ''):
            self.send_response(code, message)
            self.send_header("Content-Type", "text/html")
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write('<meta http-equiv="refresh" content="0; URL=%s">' % self.gitweb_url)
        else:
            CGIHTTPRequestHandler.send_error(self, code, message)

    def do_HEAD(self):
        self.redirect_path()
        CGIHTTPRequestHandler.do_HEAD(self)
            
    def do_GET(self):
        self.redirect_path()
        CGIHTTPRequestHandler.do_GET(self)
            
    def do_POST(self):
        self.redirect_path()
        CGIHTTPRequestHandler.do_POST(self)
            
    def redirect_path(self):
        path = self.path
        i = path.rfind('?')
        if i >= 0:
            path, query = path[:i], path[i:]
        else:
            query = ''
        head, tail = path, ''
        temp = self.translate_path(head)
        while not os.path.exists(temp):
            i = head.rfind('/')
            if i < 0:
                break
            head, tail = head[:i], head[i:] + tail
        self.path = head + tail + query

    def translate_path(self, path):
            path = posixpath.normpath(unquote(path))
            n = len(self.aliases)
            for i in range(n):
                url, dir = self.aliases[n-i-1]
                length = len(url)
                if path[:length] == url:
                    return dir + path[length:]
            return ''

def main():
    usage = "usage: %prog [options] <dir>"
    parser = OptionParser(usage=usage, version="%prog " + "%s" % __version__)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=True,
                      help="print status messages to stdout")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose",
                      help="don\'t print anything to stdout")
    parser.add_option("-p", "--port",
                      dest="port", type="int",
                      help="port to listen on (default: 8000)", default=8000)
    parser.add_option("-a", "--address",
                      dest="address", default="",
                      help="address to listen on (default: hostname)")
    parser.add_option("-l", "--local",
                      action="store_true", dest="local", default=False,
                      help="only listen on 127.0.0.1")
    parser.add_option("-b", "--browser",
                      action="store_true", dest="browser", default=False,
                      help="open default browser automatically")
    parser.add_option("-d", "--daemon",
                      action="store_true", dest="daemon", default=False,
                      help="detach from terminal and become a daemon")
    parser.add_option("--pid-file",
                      dest="pidfile", default="",
                      help="write the spawned process-id to this file")
    parser.add_option("--gitweb",
                      dest="gitweb", default="",
                      help="use this gitweb cgi file instead of the included version")
    (options, args) = parser.parse_args()

    # get path to gitweb.cgi file
    gitweb_cgi = options.gitweb
    if not gitweb_cgi:
        gitweb_cgi = resource_filename('gitserve', 'gitweb.cgi')
    if not os.access(gitweb_cgi, os.X_OK):
        parser.error("Your gitweb.cgi is not executable. Try 'chmod +x %s'" % gitweb_cgi)

    if len(args) > 1:
        parser.error("incorrect number of arguments")
    if args:
        repo_dir = args[0]
    else:
        repo_dir = "."

    # parse ~ directories and get name of the directory with the repositories
    if repo_dir.startswith("~"):
        repo_dir = os.path.expanduser(repo_dir)
    repo_dir = os.path.abspath(repo_dir)
    repo_name = repo_dir.split(os.path.sep)[-1]
    os.environ['GITWEB_HOME_LINK_STR'] = repo_dir

    # set env variable for the project root path
    if os.path.exists(repo_dir):
        os.environ['GITWEB_PROJECTROOT'] = repo_dir
    else:
        parser.error("repository directory doesn't exist")

    # set env variable for the project root path
    if os.path.exists(os.path.expanduser('~/.gitwebconfig')):
        gitweb_conf = os.path.expanduser('~/.gitwebconfig')
    else:
        gitweb_conf = resource_filename('gitserve', 'gitweb.conf')
    os.environ['GITWEB_CONFIG'] = gitweb_conf

    # get hostname from the system and build url
    try:
        if options.local:
            options.address = '127.0.0.1'
        elif not options.address:
            options.address = gethostname()
        else:
            options.address = gethostbyaddr(options.address)[0]
    except SocketError, e:
        parser.error(e)
    gitweb_url = "http://%s:%d/%s/" % (options.address, options.port, repo_name)
    
    # start daemon mode
    if options.daemon:
        options.verbose = False
        become_daemon(home=repo_dir)

    # write pidfile when in daemon mode
    if options.pidfile:
        fp = open(options.pidfile, "w")
        fp.write("%d\n" % os.getpid())
        fp.close()

    GitWebRequestHandler.gitweb_url = gitweb_url
    GitWebRequestHandler.verbose = options.verbose
    GitWebRequestHandler.cgi_directories.append('/%s' % repo_name)
    GitWebRequestHandler.aliases.append(('/%s' % repo_name, gitweb_cgi))
    httpd = HTTPServer((options.address, options.port), GitWebRequestHandler)

    if options.verbose:
        print "starting gitweb at: %s" % gitweb_url

    if options.browser:
        webbrowser.open(gitweb_url)

    # start server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except SocketError:
        if options.verbose:
            raise

if __name__ == "__main__":
    main()
