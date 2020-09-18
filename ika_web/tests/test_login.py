import json

from ika_web.tests.BaseCase import BaseCase

class TestUserLogin(BaseCase):

    def test_successful_login(self):
        # Given
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post('/api/v1/auth/signup-test', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/api/v1/auth/login-test', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)