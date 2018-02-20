from google.appengine.ext import ndb
from google.appengine.api import users, mail, taskqueue


class Topic(ndb.Model):
    user_id = ndb.StringProperty()

    title = ndb.StringProperty()
    content = ndb.TextProperty()

    create_time = ndb.DateTimeProperty(auto_now_add=True)
    update_time = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @staticmethod
    def delete_topic(topic_id):
        user = users.get_current_user()
        admin = users.is_current_user_admin()
        topic = Topic.get_by_id(int(topic_id))

        if user.email() == topic.user_id or admin:
            topic.deleted = True
            # save "deleted" topic to database
            topic.put()


class Comment(ndb.Model):
    user_id = ndb.StringProperty()
    topic_id = ndb.StringProperty()

    content = ndb.TextProperty()

    create_time = ndb.DateTimeProperty(auto_now_add=True)
    update_time = ndb.DateTimeProperty(auto_now=True)
    delete_time = ndb.BooleanProperty(default=False)

    @staticmethod
    def save_comment(topic_id, content):
        email = users.get_current_user().email()

        # create new comment and save it to database
        new_comment = Comment(user_id=email, content=content, topic_id=topic_id)
        new_comment.put()

        topic = Topic.get_by_id(int(topic_id))

        taskqueue.add(url="/task/send-new-comment-mail",
                      params={
                          "topic_author_email": topic.user_id,
                          "comment_author_email": email
                      })

    # staticmethods should be the methods that don't need access to other
    # methods and data in class
    # can be called on class itself or class instance
    @staticmethod
    def get_related_topic_title(topic_id):
        topic_title = Topic.get_by_id(int(topic_id)).title
        return topic_title
