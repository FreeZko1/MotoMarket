import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import io  # Import the io module
import sys
import os

# Assuming your vehicles module is named vehicles_module.py
sys.path.append(os.path.join(os.path.dirname(__file__),".."))

from WEB.vehicles import vehicles

class TestVehiclesBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(vehicles)
        self.client = self.app.test_client()
        
        # Patch database and session
        self.db_patch = patch('DB.database_connection.DatabaseConnection')
        self.mock_db_connection = self.db_patch.start()
        self.mock_db = self.mock_db_connection().connect()
        self.mock_cursor = self.mock_db.cursor(dictionary=True)
        self.mock_cursor.fetchone.return_value = None  # Default to no data found unless specified
        self.session = patch('flask.session', new_callable=MagicMock)

    def tearDown(self):
        self.db_patch.stop()
        self.session.stop()

    def test_home_route(self):
        """Test the home route where vehicles are listed."""
        # Setup mock return value
        self.mock_cursor.fetchall.return_value = [
            {'VehicleID': 1, 'Brand': 'Toyota', 'Model': 'Corolla', 'YearOfManufacture': 2020, 'Mileage': 10000, 'Price': 15000, 'ImageData': None}
        ]
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Toyota', response.data)  # Check if vehicle brand is rendered in the response

    def test_serve_image_found(self):
        """Test serving an image for a vehicle."""
        self.mock_cursor.fetchone.return_value = {'ImageData': b'somebinarydata'}
        response = self.client.get('/image/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/jpeg')

    def test_serve_image_not_found(self):
        """Test image request for non-existent vehicle."""
        self.mock_cursor.fetchone.return_value = None
        response = self.client.get('/image/999')
        self.assertEqual(response.status_code, 404)

    def test_add_vehicle_not_logged_in(self):
        """Test adding a vehicle without being logged in."""
        with self.app.test_client() as client:
            response = client.post('/add-vehicle', data={
                'brand': 'Toyota', 'model': 'Camry', 'year': '2021', 'mileage': '5000', 'price': '30000', 'image': None
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('/login' in response.headers['Location'])
    
    def test_add_vehicle_success(self):
        """Test successful addition of a vehicle."""
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            self.mock_cursor.lastrowid = 1  # Simulate auto-increment ID of the inserted vehicle
            response = client.post('/add-vehicle', data={
                'brand': 'Honda', 'model': 'Civic', 'year': '2020', 'mileage': '100', 'price': '20000', 'image': (io.BytesIO(b'image data'), 'test.jpg')
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            # Convert byte data to a Unicode string
            response_text = response.get_data(as_text=True)
            self.assertIn('Vozidlo bylo úspěšně přidáno.', response_text)

if __name__ == '__main__':
    unittest.main()
