import os
import unittest
import webapp2
import webtest
# uuid generates random tokens
import uuid

from google.appengine.api import memcache

from google.appengine.ext import testbed
from models.models import Topic, Comment, Subscription
from main import app


class TopicTests(unittest.TestCase):
    def setUp(self):

        # instantiate TestApp with app to include all the Routes in app
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_topic_add_handler(self):
        # GET
        get = self.testapp.get('/topic/add')
        self.assertEqual(get.status_int, 200)

        # POST
        csrf_token = str(uuid.uuid4())  # convert UUID to string
        memcache.add(key=csrf_token, value=True, time=600)

        title = "Some new topic"
        content = "This is a new topic. Just for testing purposes."

        params = {"title": title, "content": content, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/add', params)  # do a POST request
        self.assertEqual(post.status_int, 302)  # 302 means "redirect" - this is what we do at the end of POST method in TopicAdd handler

        topic = Topic.query().get()  # get the topic create by this text (it's the only one in this fake database)
        self.assertEqual(topic.title, title)  # check if topic title is the same as we wrote above
        self.assertEqual(topic.content, content)

    def test_topic_details_handler(self):
        # Create test topic
        title = "Some new topic"
        content = "This is a new topic. Just for testing purposes."

        topic = Topic(
            user_id=os.environ['USER_EMAIL'],
            title = title,
            content = content
        )
        topic.put()

        # GET
        topic = Topic.query().get()
        get = self.testapp.get('/topic/details/' + str(topic.key.id()))
        self.assertEqual(get.status_int, 200)
        self.assertEqual(topic.title, title)

        # POST
        # 1. POST test comment via '/topic/details/<topic_id>'
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=True, time=600)
        content = "This is a new comment. Just for testing purposes."

        params = {"content": content, "csrf_token": csrf_token}

        # topic_id is extracted from request when creating comment via TopicDetails handler
        # Comment.save_comment(topic_id, content)
        post = self.testapp.post('/topic/details/' + str(topic.key.id()), params)
        self.assertEqual(post.status_int, 302)

        comment = Comment.query().get()
        self.assertEqual(comment.content, content)

        # 2. POST test subscription via '/topic/details/<topic_id>'
        params = {"csrf_token": csrf_token}

        # topic_id is extracted from request when creating comment via TopicDetails handler
        # Subscription.save_comment(topic_id, user_id)
        post = self.testapp.post('/topic/details/' + str(topic.key.id()), params)
        self.assertEqual(post.status_int, 302)

        subscription = Subscription.query().get()
        self.assertEqual(subscription.user_id, os.environ['USER_EMAIL'])

    def test_topic_delete_handler(self):
        # Create test topic
        title = "Some new topic"
        content = "This is a new topic. Just for testing purposes."

        topic = Topic(
            user_id=os.environ['USER_EMAIL'],
            title = title,
            content = content
        )
        topic.put()

        # Delete test topic via '/topic/delete/<topic_id>'
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=True, time=600)
        topic = Topic.query().get()

        params = {"csrf_token": csrf_token}

        post = self.testapp.post('/topic/delete/' + str(topic.key.id()), params)
        self.assertEqual(post.status_int, 302)
        # check if topic.deleted field was set to True
        self.assertEqual(topic.deleted, True)
