# imports
import webapp2

# local imports
from handlers.main_handler import MainHandler
from handlers.cookie_handler import CookieHandler
from handlers.topic_handlers import AddTopic, DeleteTopic, TopicDetails
from workers.mail_worker import MailWorker


# url routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="set-cookie"),
    webapp2.Route('/topic/add', AddTopic, name="add-topic"),
    webapp2.Route('/topic/delete/<topic_id>', DeleteTopic, name="delete-topic"),
    webapp2.Route('/topic/details/<topic_id>', TopicDetails, name="topic-details"),
    webapp2.Route('/task/send-new-comment-mail', MailWorker, name="mail-worker"),
], debug=True)
