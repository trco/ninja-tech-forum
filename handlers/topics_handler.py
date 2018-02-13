from google.appengine.api import users

from handlers.base_handler import BaseHandler
from models.models import Topic


class AddTopicHandler(BaseHandler):
    # get is called when /add-topic is run
    def get(self):
        return self.render_template("add_topic.html")

    # post is called when add topic form is submitted
    def post(self):

        user = users.get_current_user()

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        email = users.get_current_user().email()
        title = self.request.get("title")
        content = self.request.get("content")

        # user_id can't be retrived from google.appengine.api
        new_topic = Topic(user_id=email, title=title, content=content)
        # save topic to database
        new_topic.put()

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())

class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        params = {
            "topic": topic
        }
        return self.render_template("topic_details.html", params)
