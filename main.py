# imports
import webapp2

# local imports
from handlers.main_handler import MainHandler
from handlers.cookie_handler import CookieHandler
from handlers.topic_handlers import AddTopic, TopicDetails
from handlers.comment_handlers import AddComment

# url routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="set-cookie"),
    webapp2.Route('/topic/add', AddTopic, name="add-topic"),
    webapp2.Route('/topic/details/<topic_id>', TopicDetails, name="topic-details"),
    webapp2.Route('/comment/add', AddComment, name="add-comment"),
], debug=True)
