# imports
import webapp2

# local imports
from handlers.base import MainHandler, CookieHandler

# url routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler),
], debug=True)
