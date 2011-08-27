# bind #

bind is a framework for writing Python bindings for web services. The aim of bind is to make writing web service bindings fast and simple, and to make it easy for maintainers of bindings to keep up with constantly changing and growing APIs.

Defining an API in bind is very similar to defining a database table in many popular Python ORMs like SQLAlchemy or the Django ORM. Here's a sample binding:

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

## Is bind stable? Can I get it on PyPI (the Cheeseshop)? ##

No and no. Right now, bind is at a "prototype" release. This release is to get the module out there for experimentation and hacking and to raise awareness. I won't put anything on PyPI (and, consequentially, write a setup script) until bind reaches stability.

## Contributing ##

Forks/patches/contributions are always welcome. If you're working on fixing a bug or implementing a feature not on the list of planned feature, happy hacking! If you're working on a planned feature, make sure you check the list of branches to make sure that I'm not already working on it. If I am, send me a message and I'll try to coordinate our efforts.

## Help ##

Check out [the example](http://github.com/RafeKettler/bind/master/example.py), send me a message on GitHub, or contact me directly at rafe.kettler AT gmail DOT COM.


