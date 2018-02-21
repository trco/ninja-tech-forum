from google.appengine.api import mail

from handlers.base_handler import BaseHandler


class MailWorker(BaseHandler):
    def post(self):
        to = self.request.get("receiver")
        comment_author_email = self.request.get("comment_author_email")

        mail.send_mail("info@ninjaforum.si",
                        to,
                        "New comment on Ninja-Tech-Forum",
                        "<b>%s</b> added comment." % comment_author_email)
