from handlers.base_handler import BaseHandler
from models.models import Topic


class MainHandler(BaseHandler):
    def get(self):
        topics = Topic.query().order(-Topic.create_time)

        params = {
            "topics": topics
        }
        return self.render_template("home.html", params)
