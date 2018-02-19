from handlers.base_handler import BaseHandler
from models.models import Topic


class MainHandler(BaseHandler):
    def get(self):
        # fetch saves data to topics variable so the next database query
        # doesn't have to be performed if needed
        topics = Topic.query(Topic.deleted == False).order(-Topic.create_time).fetch()

        params = {
            "topics": topics
        }
        return self.render_template("home.html", params)
