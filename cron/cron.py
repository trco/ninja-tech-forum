from datetime import datetime, timedelta

from handlers.base_handler import BaseHandler
from models.models import Topic


class TopicsDeleteCron(BaseHandler):
    def get(self):
        time_delete = datetime.now() - timedelta(days=30)

        topics_to_delete = Topic.query(
            Topic.deleted == True,
            Topic.deleted_time != None,
            Topic.deleted_time < time_delete).fetch()
        for topic in topics_to_delete:
            topic.key.delete()
