"""
bind -- a framework for creating web service API bindings in Python.

bind -- the core of the bind framework

Copyright (c) 2011 Rafe Kettler

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import urlparse
import httplib2
import re
import base64

class URLPattern(object):
    """A URL pattern. Patterns are of the form:

           /path/:param/otherpath/day:param2/

    A section of a path can begin with a ':' to indicate a parameter in
    the URL. A parameter consumes characters until the next '/'. Patterns
    cannot be absolute paths, only relative."""
    param_pattern = re.compile(r':(\w+)')

    def __init__(self, pattern):
        self.pattern = pattern
        self.parse()

    def parse(self):
        """Parse the provided URL pattern into static and dynamic
        components. The resulting attribute, self.parameters, is a list of
        tuples. Each tuple contains two elements: the value of that part of
        the URL pattern, and a dictionary containing a key "dynamic" mapped
        to a boolean value telling the URLPattern whether that particular
        part of the URL must be replaced. Dynamic components also have a
        key "param" which contains the name of the parameter (e.g. "foo" if
        the parameter were ":foo"."""
        self.parameters = []
        for parameter in self.pattern.split('/'):
            match = self.param_pattern.match(parameter)
            if match is None:
                self.parameters.append((parameter, {"dynamic":False}))
            else:
                self.parameters.append((parameter, {"dynamic":True,
                                                     "param":match.group(1)}
                                                     ))

    def make_url(self, **kw):
        """Make a URL based on the pattern. Takes keyword arguments based
        on the parameters of the URL pattern."""
        tojoin = []
        for parameter, info in self.parameters:
            if info['dynamic']:
                tojoin.append(kw.pop(info['param']))
            else:
                tojoin.append(parameter)
        return '/'.join(tojoin)

class Request(object):
    """Represents a request to an API."""
    def __init__(self, pattern, method="GET", base_url=None,
                 requires_auth=False, request_callback=None,
                 response_callback=None):
        self.requires_auth = requires_auth
        if self.requires_auth:
            self.username, self.password = None, None
        self.base_url = base_url
        self.pattern = URLPattern(pattern)
        self.http = httplib2.Http()
        self.method = "GET"
        # If request_callback or response_callback arguments were not supplied,
        # provide default callbacks that do nothing
        default_callback = lambda x, y: (x, y)
        request_callback = request_callback or default_callback 
        response_callback = response_callback or default_callback
        # Callback attributes need to be staticmethods so that they don't
        # get passed self when called by an instance
        self.request_callback = staticmethod(request_callback)
        self.response_callback = staticmethod(response_callback)

    def authenticate(self, username, password):
        """Set up to authenticate using HTTP basic authentication. Note
        that this just sets up to authenticate, the method does not
        perform any requests."""
        self.username, self.password = username, password
        authstring = base64.encodestring(self.username + ":" +
                                         self.password)
        self.auth_header = "Basic " + authstring

    def set_base_url(self, url):
        """Set the base URL for requests."""
        # If the base URL was explicitly set in the constructor, don't
        # change it
        if self.base_url is None:
            self.base_url = url            

    def request(self, body=None, headers={}, **params):
        """Make an HTTP request. Takes keyword arguments based on the
        instance's URL pattern. Returns a tuple (response, content)."""
        relative_url = self.pattern.make_url(**params)
        absolute_url = self.base_url + relative_url
        print absolute_url
        if self.requires_auth:
            # Add HTTP basic auth headers
            headers['Authorization'] = self.auth_header
        headers, body = self.request_callback(headers, body)
        response, content = self.http.request(absolute_url, self.method,
                                              body, headers)
        return self.response_callback(response, content)

    def __call__(self, *args, **kw):
        """Alias for self.request. Allows convenient API call methods, e.g.
        ``myapi.do_some_request(*args, **kw)`` instead of
        ``myapi.do_some_request.request(*args, **kw)``."""
        return self.request(*args, **kw)

class API(object):
    """Represents an API."""
    POSSIBLE_GLOBAL_ATTRS = ["BASE_URL", "REQUEST_CALLBACK",
                             "RESPONSE_CALLBACK"]

    def __init__(self):
        # Set any globally defined attributes for the Request class
        # attributes
        global_attrs = []
        for attr in self.POSSIBLE_GLOBAL_ATTRS:
            if getattr(self, attr, False):
                global_attrs.append(attr)
        for req in self.__class__.__dict__.values():
            if isinstance(req, Request):
                if "BASE_URL" in global_attrs:
                    req.set_base_url(self.BASE_URL)
                if "REQUEST_CALLBACK" in global_attrs:
                    req.request_callback = self.REQUEST_CALLBACK
                if "RESPONSE_CALLBACK" in global_attrs:
                    req.response_callback = self.RESPONSE_CALLBACK

    def authenticate(self, username, password):
        """Authenticate using basic HTTP authentication."""
        for req in self.__class__.__dict__.values():
            if isinstance(req, Request):
                if req.requires_auth:
                    req.authenticate(username, password)
