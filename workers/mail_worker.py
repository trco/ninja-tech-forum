from google.appengine.api import mail

from handlers.base_handler import BaseHandler


class MailWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get("topic_author_email")
        comment_author_email = self.request.get("comment_author_email")

        mail.send_mail("info@ninjaforum.si",
                        topic_author_email,
                        "New comment on Ninja-Tech-Forum",
                        "<b>%s</b> added comment to your topic." % comment_author_email)
