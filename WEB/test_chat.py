import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, template_rendered, session
import sys
import os

# Assuming your vehicles module is named vehicles_module.py
sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from WEB.chat import chat

class ChatTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(chat)
        self.app.secret_key = 'test'
        self.client = self.app.test_client()

        self.db_patch = patch('DB.database_connection.DatabaseConnection')
        self.mock_db_connection = self.db_patch.start()
        self.mock_db = self.mock_db_connection().connect()
        self.mock_cursor = self.mock_db.cursor(dictionary=True)

    def tearDown(self):
        self.db_patch.stop()

    def test_chat_page(self):
        with self.client:
            response = self.client.get('/chat-with/2')
            self.assertEqual(response.status_code, 200)

    def test_send_message_success(self):
        with self.client:
            self.mock_cursor.execute.return_value = None
            self.mock_db.commit.return_value = None
            response = self.client.post('/api/send-message', data={'sender_id': '1', 'recipient_id': '2', 'text': 'Hello'})
            self.assertEqual(response.json['success'], True)

    def test_send_message_failure_missing_fields(self):
        with self.client:
            response = self.client.post('/api/send-message', data={'sender_id': '1'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json['success'], False)

    def test_get_messages(self):
        with self.client:
            self.mock_cursor.fetchall.return_value = [{'MessageText': 'Hello', 'Timestamp': '2021-01-01 12:00:00', 'FirstName': 'John', 'LastName': 'Doe'}]
            response = self.client.get('/api/messages/1/2')
            self.assertEqual(response.json[0]['MessageText'], 'Hello')

    def test_chat_list_not_logged_in(self):
        with self.client:
            session.clear()
            response = self.client.get('/chat-list')
            self.assertRedirects(response, '/login')

    def test_chat_list_logged_in(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['user_id'] = 1
            self.mock_cursor.fetchall.return_value = [{'UserID': '2', 'FirstName': 'John', 'LastName': 'Doe'}]
            response = self.client.get('/chat-list')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
