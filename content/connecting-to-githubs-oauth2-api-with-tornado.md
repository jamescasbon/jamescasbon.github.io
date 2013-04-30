Title: Connecting to Github's OAuth2 API with Tornado
Date: 2012-06-03 10:20
Category: Python
Tags: python, tornado
Slug: connecting-to-githubs-oauth2-api-with-tornado
Author: James Casbon
Summary: Short version for index and feeds

Github has a nice OAuth2 API that we can use to manipulate git repos, gists,
etc.  I went through the process of implementing a Tornado based client for the
API.  This could allow a github backed application.  Note here, we are still
performing server side operations, so the client is relatively simple.  An
alternative approach is to do the github interaction in the browser.  If you are
interested in that, check this library.

Tornado takes a callback based approach, and we need to code the entire OAuth2
dance in this way.  There is an base class, tornado.auth.OAuth2Mixin, which can
perform a very small subset of the protocol.  The steps we need to log in a
user:

1. Get an authorization code using authorize_redirect method from the base class.
This presents the user with a 'do you want to authorize this app dialog in
github'.  Github then posts back to our app with the code

2. Get a user access token by exchanging the code for an access token.  This is
done via a simple GET.  This means the user is now logged in.

3. Get the user details by asking the API for the user information

4. Parse the user information and store the relevant details in a session/whatever

Here is a base class that takes care of many of these details.
get_authenticated_user needs an authorization code, which it uses to get an
access token.  If it succeeds, it calls _on_access_code, which makes an API
request to /user.  This is then returned to the callback set by the original
caller of get_authenticated_user.  It also provides github_request, which makes
an API call and hands the data to _parse_response which in turn hands it to the
callback specified by the caller.

https://gist.github.com/2962341.js?file=github.py

We can use this, as below, to create handlers to login a user - and in this case
store the credentials in a secure cookie - or to make an API call for a logged
in user:

https://gist.github.com/2962341.js?file=example.py

