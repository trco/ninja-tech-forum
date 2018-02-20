from google.appengine.api import users

from models.models import Comment
from handlers.base_handler import BaseHandler


class UserComments(BaseHandler):
    def get(self):
        user = users.get_current_user()

        user_comments = Comment.query(
            Comment.user_id == user.email()).order(-Comment.create_time).fetch()

        params = {
            "user_comments": user_comments
        }

        return self.render_template("user_comments.html", params)
