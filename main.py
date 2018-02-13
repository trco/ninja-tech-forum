# imports
import webapp2

# local imports
from handlers.main_handler import MainHandler
from handlers.cookie_handler import CookieHandler
from handlers.topics_handler import AddTopicHandler, TopicDetailsHandler

# url routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="set-cookie"),
    webapp2.Route('/topic/add', AddTopicHandler, name="add-topic"),
    webapp2.Route('/topic/details/<topic_id>', TopicDetailsHandler, name="topic-details"),
], debug=True)
