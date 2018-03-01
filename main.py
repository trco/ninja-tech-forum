# imports
import webapp2

# local imports
from handlers.main_handler import MainHandler
from handlers.cookie_handler import CookieHandler
from handlers.topic_handlers import AddTopic, DeleteTopic, TopicDetails
from handlers.comment_handlers import UserComments, DeleteComment, CountComments
from handlers.subscription_handler import SubscribeLatestTopics
from workers.mail_worker import MailWorker, MailWorkerTopics
from cron.cron import TopicsDeleteCron, NotifyOnLatestTopicsCron, CommentsDeleteCron


# url routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="set-cookie"),
    # topic routes
    webapp2.Route('/topic/add', AddTopic, name="add-topic"),
    webapp2.Route('/topic/delete/<topic_id>', DeleteTopic, name="delete-topic"),
    webapp2.Route('/topic/details/<topic_id>', TopicDetails, name="topic-details"),
    webapp2.Route('/subscribe/latest-topics', SubscribeLatestTopics, name="latest-topics"),
    webapp2.Route('/task/send-new-comment-mail', MailWorker, name="mail-worker"),
    webapp2.Route('/task/send-latest-topics-mail', MailWorkerTopics, name="mail-worker-topics"),
    # comment routes
    webapp2.Route('/comment/delete/<comment_id>', DeleteComment, name="delete-comment"),
    webapp2.Route('/user-comments', UserComments, name="user-comments"),
    webapp2.Route('/count-comments/<topic_id>', CountComments, name="count-comments"),
    # crons
    webapp2.Route('/cron/topics-delete', TopicsDeleteCron, name="topics-delete"),
    webapp2.Route('/cron/comments-delete',CommentsDeleteCron, name="comments-delete"),
    webapp2.Route('/cron/notify-on-latest-topics', NotifyOnLatestTopicsCron, name="notify-on-latest-topics"),

], debug=True)
