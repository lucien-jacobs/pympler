"""
Compatibility layer to allow Pympler being used from Python 2.x and Python 3.x.
"""

import sys

# Version dependent imports

try:
    from StringIO import StringIO
    BytesIO = StringIO
except ImportError:
    from io import StringIO, BytesIO

try:
    import cPickle as pickle
except ImportError:
    import pickle  # PYCHOK Python 3.0 module

try:
    from new import instancemethod
except ImportError:  # Python 3.0
    def instancemethod(*args):
        return args[0]

try:
    from HTMLParser import HTMLParser
except ImportError:  # Python 3.0
    from html.parser import HTMLParser

try:
    from httplib import HTTPConnection
except ImportError:  # Python 3.0
    from http.client import HTTPConnection

try:
    from urllib2 import Request, urlopen, URLError
except ImportError:  # Python 3.0
    from urllib.request import Request, urlopen
    from urllib.error import URLError

try:
    from json import dumps
except ImportError:  # Python 2.5
    try:
        from simplejson import dumps
    except ImportError:  # Python 2.5 without simplejson
        dumps = lambda s: unicode(s)

# KA(csilvers): We don't use tkinter (we don't use the pympler
# refbrowser), and this causes a bizarre hang when running
# "runtests.py -j2" on OS X mavericks.  The following small program
# reproduces the hang:
#    import multiprocessing, sqlite3, _tkinter
#    def hang():
#       sqlite3.connect('/tmp/foo')
#    if __name__ == '__main__':
#       multiprocessing.Pool(2).apply_async(hang, []).get(999)
tkinter = None


# Helper functions

# Python 2.x expects strings when calling communicate and passing data via a
# pipe while Python 3.x expects binary (encoded) data. The following works with
# both:
#
#   p = Popen(..., stdin=PIPE)
#   p.communicate(encode4pipe("spam"))
#
encode4pipe = lambda s: s
if sys.hexversion >= 0x3000000:
    encode4pipe = lambda s: s.encode()


def object_in_list(obj, l):
    """Returns True if object o is in list.

    Required compatibility function to handle WeakSet objects.
    """
    for o in l:
        if o is obj:
            return True
    return False
