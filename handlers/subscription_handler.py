import webapp2

from google.appengine.api import users, memcache

from handlers.base_handler import BaseHandler
from models.models import SubscriptionLatestTopics
from decorators.decorators import csrf_check, login_check


class SubscribeLatestTopics(BaseHandler):
    @login_check
    @csrf_check
    def post(self):
        user = users.get_current_user()
        user_id = user.email()
        SubscriptionLatestTopics.save_subscription(user_id)

        return self.redirect(self.request.referer)
