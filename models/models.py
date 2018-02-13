from google.appengine.ext import ndb


class Topic(ndb.Model):
    user_id = ndb.StringProperty()

    title = ndb.StringProperty()
    content = ndb.TextProperty()

    # TODO: check arguments for DateTimeProperty !!!
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    update_time = ndb.DateTimeProperty(auto_now=True)
    delete_time = ndb.BooleanProperty(default=False)


class Comment(ndb.Model):
    user_id = ndb.StringProperty()
    topic_id = ndb.StringProperty()

    content = ndb.TextProperty()

    create_time = ndb.DateTimeProperty(auto_now_add=True)
    update_time = ndb.DateTimeProperty(auto_now=True)
    delete_time = ndb.BooleanProperty(default=False)
