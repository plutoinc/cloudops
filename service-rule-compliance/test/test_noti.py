import unittest
import noti

class NotiTest(unittest.TestCase):

    def test_notify(self):
        noti.notify("zxxx")

    def test_tag_policy(self):
        import resource_tag_policy
        resource_tag_policy.handler(None, None)