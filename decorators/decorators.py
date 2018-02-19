# memcache is database that lives in computer's RAM
from google.appengine.api import users, memcache
from models.models import Topic

def csrf_check(func):
    # self is a POST method argument and decorator needs and has access
    # to it at runtime, self points to BaseHandler in this case?
    def wrapper(self, *args, **kwargs):
        # csrf token check
        csrf_token = self.request.get("csrf_token")
        if not memcache.get(csrf_token):
            return self.write("CSRF attack in progress!")
        else:
            return func(self, *args, **kwargs)

    return wrapper

def login_check(func):
    # self is a POST method argument and decorator needs and has access
    # to it at runtime, self points to BaseHandler in this case?
    def wrapper(self, *args, **kwargs):
        # user login check
        user = users.get_current_user()
        if not user:
            return self.write("Please login before posting.")
        else:
            return func(self, *args, **kwargs)

    return wrapper
