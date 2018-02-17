import cgi
# uuid generates random tokens
import uuid

# memcache is database that lives in computer's RAM
from google.appengine.api import users, memcache

from handlers.base_handler import BaseHandler
from models.models import Topic, Comment


class AddTopic(BaseHandler):
    # get is called when /add-topic is run
    def get(self):

        params = {
            "csrf_token": str(uuid.uuid4())
        }

        # add csrf_token to memcache database
        memcache.add(params["csrf_token"], True, 60*10)

        return self.render_template("add_topic.html", params)

    # post is called when add topic form is submitted
    def post(self):
        # csrf token check
        csrf_token = self.request.get("csrf_token")
        if not memcache.get(csrf_token):
            return self.write("CSRF attack in progress!")

        user = users.get_current_user()

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        email = users.get_current_user().email()
        # cgi disables option to post html or javascript in form fields
        title = cgi.escape(self.request.get("title"))
        content = cgi.escape(self.request.get("content"))

        # user_id can't be retrived from google.appengine.api
        new_topic = Topic(user_id=email, title=title, content=content)
        # save topic to database
        new_topic.put()

        new_topic_id = new_topic.key.id()

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetails(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        params = {
            "topic": topic,
            "csrf_token": str(uuid.uuid4())
        }

        # get comments if they exist
        try:
            comments = (Comment.query(
                Comment.topic_id == topic_id,
                Comment.delete_time == False).order(-Comment.create_time).fetch()
            )
            params["comments"] = comments
        except:
            pass

        # add csrf_token to memcache database
        memcache.add(params["csrf_token"], True, 60*10)

        return self.render_template("topic_details.html", params)
