
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask import session
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
# Import your auth blueprint
from auth import auth


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(auth, url_prefix='/auth')
        self.client = self.app.test_client()
        self.app.secret_key = 'TestSecret'

        # Mock database connection
        self.db_patch = patch('DB.database_connection.DatabaseConnection')
        self.mock_db_connection = self.db_patch.start()
        self.mock_db = self.mock_db_connection().connect()
        self.mock_cursor = self.mock_db.cursor(dictionary=True)

    def tearDown(self):
        self.db_patch.stop()

    def test_login_view(self):
        """ Test the login page access """
        response = self.client.get('/auth/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('login.html', (call[0][0] for call in self.mock_render_template.call_args_list))

    def test_login_success(self):
        """ Test successful login """
        self.mock_cursor.fetchone.return_value = {'UserID': 1, 'Password': 'pass', 'Role': 'user'}
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.client.post('/auth/login', data={'loginEmail': 'user@example.com', 'loginPassword': 'pass'})
            self.assertRedirects(response, '/auth/page')
            self.assertIn('user_id', session)

    def test_login_failure(self):
        """ Test login with incorrect credentials """
        self.mock_cursor.fetchone.return_value = None
        response = self.client.post('/auth/login', data={'loginEmail': 'user@example.com', 'loginPassword': 'wrong'})
        self.assertIn('Přihlašovací údaje jsou neplatné.', response.get_data(as_text=True))

    def test_register_success(self):
        """ Test successful registration """
        self.mock_cursor.fetchone.side_effect = [None, None]  # No existing username or phone
        response = self.client.post('/auth/register', data={
            'registerUsername': 'newuser',
            'registerFirstName': 'New',
            'registerLastName': 'User',
            'registerEmail': 'newuser@example.com',
            'registerPassword': 'Password1',
            'registerPhone': '123456789'
        })
        self.assertRedirects(response, '/auth/login_view')
        self.mock_cursor.execute.assert_called()

    def test_register_failure(self):
        """ Test registration with existing username """
        self.mock_cursor.fetchone.side_effect = [{'username': 'newuser'}, None]  # Username exists
        response = self.client.post('/auth/register', data={
            'registerUsername': 'newuser',
            'registerFirstName': 'New',
            'registerLastName': 'User',
            'registerEmail': 'newuser@example.com',
            'registerPassword': 'Password1',
            'registerPhone': '123456789'
        })
        self.assertIn('Uživatelské jméno je již používáno.', response.get_data(as_text=True))

    def test_profile_access_denied(self):
        """ Test profile access without login """
        response = self.client.get('/auth/profile')
        self.assertRedirects(response, '/auth/login_view')

    def test_profile_access_success(self):
        """ Test accessing the profile when logged in """
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            self.mock_cursor.fetchone.return_value = {'UserID': 1, 'FirstName': 'John', 'LastName': 'Doe', 'Email': 'john@example.com'}
            response = self.client.get('/auth/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn('profile.html', (call[0][0] for call in self.mock_render_template.call_args_list))

    def test_logout(self):
        """ Test logging out """
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            response = self.client.get('/auth/logout')
            self.assertRedirects(response, '/auth/login_view')
            self.assertNotIn('user_id', session)

if __name__ == '__main__':
    unittest.main()
