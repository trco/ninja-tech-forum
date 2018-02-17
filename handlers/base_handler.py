import os
import jinja2
import webapp2

from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        # check if cookie exists
        if self.request.cookies.get == "YES":
            params["cookies"] = True

        # get current user
        user = users.get_current_user()
        # check if user is logged in or not
        if user:
            # create url and add it to params
            params["logout_url"] = users.create_logout_url("/")
        else:
            # create url and add it to params
            params["login_url"] = users.create_login_url("/")
        # add user to params
        params["user"] = user

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))
