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

    :::python
    import urllib
    import tornado.ioloop
    import tornado.web
    import tornado.auth
    import tornado.httpclient
    import tornado.escape
    import tornado.httputil
    import logging


    class GithubMixin(tornado.auth.OAuth2Mixin):
        """ Github OAuth Mixin, based on FacebookGraphMixin
        """

        _OAUTH_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
        _OAUTH_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
        _API_URL = 'https://api.github.com'

        def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                                code, callback, extra_fields=None):
            """ Handles the login for Github, queries /user and returns a user object
            """
            logging.debug('gau ' + redirect_uri)
            http = tornado.httpclient.AsyncHTTPClient()
            args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            }

            http.fetch(self._oauth_request_token_url(**args),
                self.async_callback(self._on_access_token, redirect_uri, client_id,
                                    client_secret, callback, fields))

        def _on_access_token(self, redirect_uri, client_id, client_secret,
                            callback, fields, response):
            """ callback for authentication url, if successful get the user details """
            if response.error:
                logging.warning('Github auth error: %s' % str(response))
                callback(None)
                return

            args = tornado.escape.parse_qs_bytes(
                    tornado.escape.native_str(response.body))

            if 'error' in args:
                logging.error('oauth error ' + args['error'][-1])
                raise Exception(args['error'][-1])

            session = {
                "access_token": args["access_token"][-1],
            }

            self.github_request(
                method="/user",
                callback=self.async_callback(
                    self._on_get_user_info, callback, session),
                access_token=session["access_token"],
                )

        def _on_get_user_info(self, callback, session, user):
            """ callback for github request /user to create a user """
            logging.debug('user data from github ' + str(user))
            if user is None:
                callback(None)
                return
            callback({
                "login": user["login"],
                "name": user["name"],
                "email": user["email"],
                "access_token": session["access_token"],
            })

        def github_request(self, path, callback, access_token=None,
                    method='GET', body=None, **args):
            """ Makes a github API request, hands callback the parsed data """
            args["access_token"] = access_token
            url = tornado.httputil.url_concat(self._API_URL + path, args)
            logging.debug('request to ' + url)
            http = tornado.httpclient.AsyncHTTPClient()
            if body is not None:
                body = tornado.escape.json_encode(body)
                logging.debug('body is' +  body)
            http.fetch(url, callback=self.async_callback(
                    self._parse_response, callback), method=method, body=body)

        def _parse_response(self, callback, response):
            """ Parse the JSON from the API """
            if response.error:
                logging.warning("HTTP error from Github: %s", response.error)
                callback(None)
                return
            try:
                json = tornado.escape.json_decode(response.body)
            except Exception:
                logging.warning("Invalid JSON from Github: %r", response.body)
                callback(None)
                return
            if isinstance(json, dict) and json.get("error_code"):
                logging.warning("Facebook error: %d: %r", json["error_code"],
                                json.get("error_msg"))
                callback(None)
                return
            callback(json)



We can use this, as below, to create handlers to login a user - and in this case
store the credentials in a secure cookie - or to make an API call for a logged
in user:

    :::python
    import tornado.ioloop
    import tornado.web
    import tornado.escape
    import tornado.options
    import tornado.httputil
    import jinja2
    import pyjade.compiler
    import coffeescript
    import markdown

    import github


    class GithubLoginHandler(tornado.web.RequestHandler, github.GithubMixin):

        _OAUTH_REDIRECT_URL = 'http://localhost:8888/auth/github'

        @tornado.web.asynchronous
        def get(self):
            # we can append next to the redirect uri, so the user gets the
            # correct URL on login
            redirect_uri = tornado.httputil.url_concat(
                    self._OAUTH_REDIRECT_URL, {'next': self.get_argument('next', '/')})

            # if we have a code, we have been authorized so we can log in
            if self.get_argument("code", False):
                self.get_authenticated_user(
                    redirect_uri=redirect_uri,
                    client_id=self.settings["github_client_id"],
                    client_secret=self.settings["github_secret"],
                    code=self.get_argument("code"),
                    callback=self.async_callback(self._on_login)
                )
                return

            # otherwise we need to request an authorization code
            self.authorize_redirect(
                    redirect_uri=redirect_uri,
                    client_id=self.settings["github_client_id"],
                    extra_params={"scope": self.settings['github_scope'], "foo":1})

        def _on_login(self, user):
            """ This handles the user object from the login request """
            if user:
                logging.info('logged in user from github: ' + str(user))
                self.set_secure_cookie("user", tornado.escape.json_encode(user))
            else:
                self.clear_cookie("user")
            self.redirect(self.get_argument("next","/"))


    class GistLister(BaseHandler, github.GithubMixin):

        @tornado.web.authenticated
        @tornado.web.asynchronous
        def get(self):
            self.github_request(
                    '/gists', self._on_get_gists,
                    access_token=self.current_user['access_token'])

        def _on_get_gists(self, gists):
            self.render('gists.jade', gists=gists)
