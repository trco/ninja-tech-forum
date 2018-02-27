import os
import unittest
import webapp2
import webtest
# uuid generates random tokens
import uuid

from google.appengine.api import memcache

from google.appengine.ext import testbed
from models.models import Topic, Comment
from main import app


class CommentTests(unittest.TestCase):
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

    def test_user_comments_handler(self):
        # GET
        get = self.testapp.get('/user-comments')
        self.assertEqual(get.status_int, 200)

    def test_comment_delete_handler(self):
        # POST test topic via '/topic/add'
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=True, time=600)

        title = "Some new topic"
        content = "This is a new topic. Just for testing purposes."

        params = {"title": title, "content": content, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/add', params)
        self.assertEqual(post.status_int, 302)

        # POST test comment via '/topic/details/<topic_id>'
        content = "This is a new comment. Just for testing purposes."

        params = {"content": content, "csrf_token": csrf_token}

        topic = Topic.query().get()
        # topic_id is extracted from request when creating comment via TopicDetails handler
        # Comment.save_comment(topic_id, content)
        post = self.testapp.post('/topic/details/' + str(topic.key.id()), params)
        self.assertEqual(post.status_int, 302)

        # Delete comment via '/comment/delete/<comment_id>'
        comment = Comment.query().get()
        params = {"csrf_token": csrf_token}

        post = self.testapp.post('/comment/delete/' + str(comment.key.id()), params)
        self.assertEqual(post.status_int, 302)
        # check if comment.deleted field was set to True
        self.assertEqual(comment.deleted, True)
