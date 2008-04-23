#!/usr/bin/python
# encoding: utf-8

__version__ = '0.1.0'

import os
import sys
import stat
import signal
import urllib
import urlparse
import posixpath
import webbrowser
import CGIHTTPServer
import BaseHTTPServer

class RequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    gitserve_dir = os.path.dirname(os.path.abspath(__file__))
    indices = [
        'index.html', 
        'index.cgi', 
        'index.pl', 
        'index.php', 
        'index.xhtml',
    ]
    
    aliases = [
        ('/', './'),
        ('/cgi-bin', os.path.join(gitserve_dir, "cgi-bin")),
        ('/media', os.path.join(gitserve_dir, "media")),
    ]
    
    actions = {
        'application/x-httpd-php': '/cgi-bin/php4',
    }

    CGIHTTPServer.CGIHTTPRequestHandler.extensions_map.update({
        '.php': 'application/x-httpd-php',
    })
    
    def do_HEAD(self):
        self.redirect_path()
        CGIHTTPServer.CGIHTTPRequestHandler.do_HEAD(self)
            
    def do_GET(self):
        self.redirect_path()
        CGIHTTPServer.CGIHTTPRequestHandler.do_GET(self)
            
    def do_POST(self):
        self.redirect_path()
        CGIHTTPServer.CGIHTTPRequestHandler.do_POST(self)
            
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
            temp = self.translate_path(head)

        if os.path.isdir(temp):
            for index in self.indices:
                if os.path.exists(os.path.join(temp, index)):
                    head = posixpath.join(head, index)
                    break

        ctype = self.guess_type(head)
        if ctype in self.actions:
            os.environ['REDIRECT_STATUS'] = '200'                   
            head = self.actions[ctype] + head

        self.path = head + tail + query

    def translate_path(self, path):
            path = posixpath.normpath(urllib.unquote(path))
            n = len(self.aliases)
            for i in range(n):
                url, dir = self.aliases[n-i-1]
                length = len(url)
                if path[:length] == url:
                    return dir + path[length:]
            return ''

def runserver(htdocs=os.getcwd()):
    "Use default port 8000 or port given in cmd"
    if len(sys.argv) == 1:
        port = 8000
    else:
        port = int(sys.argv[1])
    addr = "127.0.0.1"
    root_url = "http://%s:%d/" % (addr, port)

    os.environ['GITWEB_CONFIG'] = os.path.join(
        RequestHandler.gitserve_dir, "media", "gitweb.conf")

    def onSignal(sign, stack):
        """Signal handler for save exit"""
        sys.exit(0)
    signal.signal(signal.SIGINT, onSignal)

    httpd = BaseHTTPServer.HTTPServer((addr, port), RequestHandler)
    webbrowser.open(urlparse.urljoin(root_url, "cgi-bin/gitweb.cgi"))
    httpd.serve_forever()

def main():
    runserver()

if __name__ == "__main__":
    sys.exit(main())
