# bind #

bind is a framework for writing Python bindings for web services. The aim of bind is to make writing web service bindings fast and simple, and to make it easy for maintainers of bindings to keep up with constantly changing and growing APIs.

Defining an API in bind is very similar to defining a database table in many popuplar Python ORMS like SQLAlchemy or the Django ORM. Here's a sample binding:

    from bind import Request, API
    
    class MyAPI(API):
        BASE_URL = "http://mysite.com/api"

	get_user_info = Request("/users/:user", "GET")
	set_user_info = Request("/users/:user", "POST", requires_auth=True)
	...

Usage is equally simple:

    # Create a client for our API
    api = MyAPI()
    # Make an API call
    user_info = api.get_user_info(user="Jane")
    # Make some changes to our user info for Jane
    ...
    # Now, let's authenticate and change some info
    api.authenticate("<Jane's username>", "<Jane's password>")
    api.set_user_info(changed_user_info, user="Jane")

## What does bind do, exactly? ##

bind contains a lot of the boilerplate necessary to write a web service binding. bind handles URLs, making HTTP requests, and authentication (currently only HTTP basic authentication is supported, but more is planned). bind also can abstract over processing request and response data through request and response callbacks that manipulate the data supplied by the API user and the response that the server sends back. A few common callbacks are already built in to bind (for example, there are callbacks for transforming a dict request into JSON and for transforming a JSON response into a dict). You can also easily define your own callbacks to suit your specific purposes.

## How is bind better? ##

Well, first off, bind requires almost no boilerplate. Most of that is already taken care of within the framework itself. You might have also noticed that our sample API binding is very concise (1-2 lines per API call) and could almost serve as documentation for our API.

Perhaps the best advantage of bind is how it allows you to rapidly create  change your binding as your API changes. Web services can change a lot, and bind makes it so that any addition or change to a single API call will almost always take only one line of code. bind makes writing and maintaining bindings a snap.

## Features ##

### Current features ###

 - Abstraction over HTTP requests and URL parsing
 - Callbacks for processing requests and responses
 - Support for basic HTTP authentication (insecure)

### Planned features ###

 - Error handling
 - OAuth support
 - A larger library of included callbacks
 - Automatic documentation generation

## The bind API ##

In lieu of full-fledged sphinx documentation (which will exist in the future, but is overkill right now), here's a brief overview of the bind API.

#### class `bind.API` ####

The base class for bind APIs.

`API.authenticate(username, password)`

Authenticate using basic HTTP authentication. This just sets up authentication, it doesn't perform any requests.

#### Subclassing `API` ####

Subclassing `API` is how you write your own API bindings with bind. You do so by defining class attributes for your subclass.

There are two kinds of class attributes that you can define in your subclass that are meaningful to bind. The first are constants that determine the general behavior of requests. Right now, there are three constants that you can define:

 - `BASE_URL` determines the base URL for API requests
 - `REQUEST_CALLBACK` is the default request callback for requests in your API
 - `RESPONSE_CALLBACK` is the default response callback for requests in your API

The other meaningful type of class attribute is an instance of `bind.Request`. Each instance represents a particular API call. The instances are callable, so use the desired method name for that particular API call as the attribute name.

Finally, you can define methods and other attributes to your heart's content to provide conveniences to the programmer or the user. bind doesn't treat these attributes specially (or at all), so feel free to define any kind of attribute.

#### class `bind.Request(pattern, method="GET", requires_auth=False, [base_url, request_callback, response_callback])` ####

An API call. In your subclass of `bind.API`, you'll define a number of instances of `Request` as class attributes that will represent API calls.

 - `pattern` is a URL relative to your base URL which may contain parameters that will be provided with each request. Patterns are of the form: 
    /path/:param/otherpath/day:param2/
A section of a path can begin with a ':' to indicate a parameter in
the URL. A parameter consumes characters until the next '/'. Patterns
cannot be absolute paths, only relative.
 - `method` is the HTTP method to be used for the request.
 - `requires_auth` is a boolean indicating whether or not the client must be authenticated to make the request.
 - `base_url` is the base URL for the request. This can override the `BASE_URL` attribute of the enclosing `API` subclass.
 - `request_callback` and `response_callback` are the functions that should be used to process requests and responses for this request, respectively. These arguments can override the enclosing `API` subclass's `REQUEST_CALLBACK` and `RESPONSE_CALLBACK` attributes (respectively) for the request.

`Request.authenticate(username, password)`

Authenticate the request using basic HTTP authentication. This justs sets up authentication, it doesn't perform any requests.

`Request.set_base_url(url)`

Set the base URL for this request to `url`.

`Request.request(body=None, headers={}. **parameters)`

Make the HTTP request described by the `Request` instance. `body` is the data to be sent to the server and `headers` is a dictionary containing headers to contain in the request.

`Request.__call__(*args, **kw)`

Alias for the `request()` method of a `Request` object. This is provided as a convenience so that class `Request` attributes of your API class can be called as methods.

#### module `bind.callbacks` ####

`bind.callbacks` contains a few callbacks for very common applications. Right now, there are three callback functions:

 - `request_to_json(headers, body)` -- turn a request with a dict as the body into JSON
 - `request_to_formdata(headers, body)` -- turn a request with a dict as the body into URL encoded form data
 - `response_to_json(response, content)` --- turn a JSON response into a dict

#### Defining your own callbacks ####

For request callbacks, a callback should take two arguments `headers` and `body` and return a tuple `(headers, body)` containing the transformed request.

For response callbacks, a callback should take two arguments `response` and `content` and return whatever data you like.

## Is bind stable? Can I get it on PyPI (the Cheeseshop)? ##

No and no. Right now, bind is at a "prototype" release. This release is to get the module out there for experimentation and hacking and to raise awareness. I won't put anything on PyPI (and, consequentially, write a setup script) until bind reaches stability.

## Contributing ##

Forks/patches/contributions are always welcome. If you're working on fixing a bug or implementing a feature not on the list of planned feature, happy hacking! If you're working on a planned feature, make sure you check the list of branches to make sure that I'm not already working on it. If I am, send me a message and I'll try to coordinate our efforts.

## Help ##

Check out [the example](http://github.com/RafeKettler/bind/master/example.py), send me a message on GitHub, or contact me directly at rafe.kettler AT gmail DOT COM.


