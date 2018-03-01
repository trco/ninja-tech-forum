from google.appengine.api import users

from models.models import Comment
from handlers.base_handler import BaseHandler
from decorators.decorators import csrf_check, login_check


class UserComments(BaseHandler):
    def get(self):
        user = users.get_current_user()

        user_comments = Comment.query(
            Comment.user_id == user.email(),
            Comment.deleted == False).order(-Comment.create_time).fetch()

        params = {
            "user_comments": user_comments
        }

        return self.render_template_with_csrf("user_comments.html", params)


class DeleteComment(BaseHandler):
    @login_check
    @csrf_check
    def post(self, comment_id):
        Comment.delete_comment(comment_id)

        return self.redirect(self.request.referer)
        # return self.redirect_to("main-page")

class CountComments(BaseHandler):
    def get(self, topic_id):
        count_comments = Comment.query(
            Comment.topic_id == topic_id,
            Comment.deleted == False).count()

        return self.write(count_comments)
