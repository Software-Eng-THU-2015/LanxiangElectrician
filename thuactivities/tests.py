# -*- coding: utf-8 -*-
"""
Tests for tornado server.
Author: Norrix
2015-11-07
"""

import main

class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        return main.make_app()
    
    def test_server_auth(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'fail')
        

