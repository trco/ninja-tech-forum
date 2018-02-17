import cgi
# uuid generates random tokens
import uuid

# memcache is database that lives in computer's RAM
from google.appengine.api import users, memcache

from handlers.base_handler import BaseHandler
from models.models import Topic, Comment


class AddComment(BaseHandler):
    # post is called when add topic form is submitted
    def post(self):
        # csrf token check
        csrf_token = self.request.get("csrf_token")
        if not memcache.get(csrf_token):
            return self.write("CSRF attack in progress!")

        # user login check
        user = users.get_current_user()
        if not user:
            return self.write("Please login before you're allowed to post a comment.")

        # get values for new comment
        # cgi disables option to post html or javascript in form fields
        # get topic_id from posted form
        email = users.get_current_user().email()
        content = cgi.escape(self.request.get("content"))
        topic_id = self.request.get("topic_id")

        # create new comment and save it to database
        new_comment = Comment(user_id=email, content=content, topic_id=topic_id)
        new_comment.put()

        # redirect to related topic details
        return self.redirect_to("topic-details", topic_id=topic_id)
