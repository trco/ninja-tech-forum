from handlers.base_handler import BaseHandler


class CookieHandler(BaseHandler):
    def post(self):
        # save info in cookie to the user's computer
        # next request will contain info from this cookie
        self.response.set_cookie("cookies-accepted", "YES")
        return self.write("Cookies accepted.")
