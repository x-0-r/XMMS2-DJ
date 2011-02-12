# -*- coding: utf-8 -*-

import unittest
from django.test.client import Client

class VolumeTestCase(unittest.TestCase):
    def testAjax(self):
        c = Client()
        response = c.get('/volume/down/20/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200, "Status Code should be 200, was %d" % response.status_code)
        self.assertTrue(response.content == 'False' or str.isdigit(response.content),
                        "Content should be 'False' or a number, but was %s" % response.content)
