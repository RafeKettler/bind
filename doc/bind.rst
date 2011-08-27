bind
======

bind is a framework for writing Python bindings for web services. The aim of bind is to make writing web service bindings fast and simple, and to make it easy for maintainers of bindings to keep up with constantly changing and growing APIs.

Defining an API in bind is very similar to defining a database table in many popuplar Python ORMS like SQLAlchemy or the Django ORM. Here's a sample binding::

    from bind import Request, API
    
    class MyAPI(API):
        BASE_URL = "http://mysite.com/api"

	get_user_info = Request("/users/:user", "GET")
	set_user_info = Request("/users/:user", "POST", requires_auth=True)
	...

Usage is equally simple::

    # Create a client for our API
    api = MyAPI()
    # Make an API call
    user_info = api.get_user_info(user="Jane")
    # Make some changes to our user info for Jane
    ...
    # Now, let's authenticate and change some info
    api.authenticate("<Jane's username>", "<Jane's password>")
    api.set_user_info(changed_user_info, user="Jane")
