"""
bind -- a framework for creating web service API bindings in Python.

bind.callbacks -- callbacks for transforming bind requests and responses

Copyright (c) 2011 Rafe Kettler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
"""

try:
    import json
except ImportError:
    print "No json module; trying simplejson instead"
    import simplejson as json
from urllib import urlencode

def request_to_json(headers, body):
    """Request callback to turn a request with a dict as the body into
    JSON."""
    headers['Content-Type'] = 'application/json'
    body = json.dumps(body)
    return headers, body

def response_to_json(response, content):
    """Response callback to turn a response with JSON content into a
    dict."""
    return json.loads(content)

def request_to_formdata(headers, body):
    """Request callback to transform a request with a dict as the body into
    URL encoded form data."""
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    body = urlencode(body)
    return headers, body
