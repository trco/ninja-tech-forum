from datetime import datetime, timedelta

from google.appengine.api import taskqueue

from handlers.base_handler import BaseHandler
from models.models import Topic, SubscriptionLatestTopics


class TopicsDeleteCron(BaseHandler):
    def get(self):
        time_delete = datetime.now() - timedelta(days=30)

        topics_to_delete = Topic.query(
            Topic.deleted == True,
            Topic.deleted_time != None,
            Topic.deleted_time < time_delete).fetch()
        for topic in topics_to_delete:
            topic.key.delete()


class CommentsDeleteCron(BaseHandler):
    def get(self):
        time_delete = datetime.now() - timedelta(days=30)

        comments_to_delete = Comment.query(
            Comment.deleted == True,
            Comment.deleted_time != None,
            Comment.deleted_time < time_delete).fetch()
        for comment in comments_to_delete:
            comment.key.delete()


class NotifyOnLatestTopicsCron(BaseHandler):
    def get(self):
        time_limit = datetime.now() - timedelta(days=1)

        latest_topics = Topic.query(
            Topic.create_time > time_limit).fetch()

        latest_topics_text = ""

        for topic in latest_topics:
            latest_topics_text = ", </br>".join(topic.title)

        subscriptions = SubscriptionLatestTopics.query().fetch()

        subscribers_list = []

        for subscription in subscriptions:
            subscribers_list.append(subscription.user_id)

        if subscribers_list:
            for subscriber in subscribers_list:
                taskqueue.add(url="/task/send-latest-topics-mail",
                              params={
                                  "latest_topics_text": latest_topics_text,
                                  "receiver": subscriber,
                              })
