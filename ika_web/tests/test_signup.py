#~/ika_web/tests/test_signup.py

import unittest
import json

import json
from ika_web.app.app import app
from ika_web.tests.BaseCase import BaseCase

class SignupTest(BaseCase):
    
    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "paurakh011@gmail.com",
            "password": "mycoolpassword"
        })

        # When
        response = self.app.post('/api/v1/auth/signup-test', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)