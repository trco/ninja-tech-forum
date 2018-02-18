import cgi

from google.appengine.api import users

from handlers.base_handler import BaseHandler
from models.models import Topic, Comment
from decorators.decorators import csrf_check, login_check


class AddTopic(BaseHandler):
    # get is called when /topic/add is run
    def get(self):
        # template is rendered with csrf_token
        return self.render_template_with_csrf("add_topic.html")

    # post is called when add topic form is submitted
    @login_check
    @csrf_check
    def post(self):
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

        return self.render_template_with_csrf("topic_details.html", params)
