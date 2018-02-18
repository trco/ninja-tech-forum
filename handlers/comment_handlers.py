import cgi
# uuid generates random tokens
import uuid

# memcache is database that lives in computer's RAM
from google.appengine.api import users, memcache

from handlers.base_handler import BaseHandler
from models.models import Topic, Comment
from decorators.decorators import csrf_check, login_check


class AddComment(BaseHandler):
    # post is called when add topic form is submitted
    @login_check
    @csrf_check
    def post(self):
        # get values for new comment from the form
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
