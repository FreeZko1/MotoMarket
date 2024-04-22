from flask import request
from flask import render_template
from flask import current_app
from DB.database_connection import DatabaseConnection
from .faq import faq_data

from flask import render_template
from werkzeug.exceptions import BadRequest

def validate_input(value, value_type, max_length=None):
    """ Pomocná funkce pro validaci vstupních hodnot. """
    if value_type == 'int':
        if value == '':
            return None  # Pokud je vstup prázdný, vrátí None
        try:
            return int(value)
        except ValueError:
            raise BadRequest(f"Hodnota {value} není validní celé číslo.")
    elif value_type == 'str':
        if value == '':
            return None  # Pokud je vstup prázdný, vrátí None
        if any(c in value for c in ";'\""):
            raise BadRequest("Neplatné znaky v textovém řetězci.")
        if max_length and len(value) > max_length:
            raise BadRequest(f"Textový řetězec je příliš dlouhý. Maximální povolená délka je {max_length}.")
        return value
    return None

def search_vehicles():
    try:
        params = {
            'brand': validate_input(request.args.get('brand', ''), 'str', 50),
            'model': validate_input(request.args.get('model', ''), 'str', 50),
            'year_min': validate_input(request.args.get('year_min', ''), 'int'),
            'year_max': validate_input(request.args.get('year_max', ''), 'int'),
            'price_min': validate_input(request.args.get('price_min', ''), 'int'),
            'price_max': validate_input(request.args.get('price_max', ''), 'int'),
            'mileage_min': validate_input(request.args.get('mileage_min', ''), 'int'),
            'mileage_max': validate_input(request.args.get('mileage_max', ''), 'int')
        }
        current_app.logger.info(f"Searching vehicles with parameters: {params}")
    except BadRequest as e:
        current_app.logger.error(f"Validation error: {e}")
        return str(e), 400

    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    query = "SELECT * FROM Vehicles WHERE 1=1"
    conditions = []
    values = []

    for field, value in params.items():
        if value is not None:
            if 'min' in field or 'max' in field:
                operator = '>=' if 'min' in field else '<='
                conditions.append(f"{field.split('_')[0]} {operator} %s")
                values.append(value)
            else:
                conditions.append(f"{field} LIKE %s")
                values.append(f"%{value}%")

    if conditions:
        query += ' AND ' + ' AND '.join(conditions)
        current_app.logger.info(f"Executing query: {query} with values: {values}")

    try:
        cursor.execute(query, values)
        vehicles = cursor.fetchall()
        current_app.logger.info(f"Found {len(vehicles)} vehicles matching criteria.")
    except Exception as e:
        current_app.logger.error(f"Database query error: {e}")
        return str(e), 500
    finally:
        cursor.close()
        db_connection.close()

    return render_template('page.html', vehicles=vehicles, faq_data=faq_data)

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from werkzeug.exceptions import BadRequest

# Tady si doimportujte funkce, které potřebujete testovat

class TestVehicleSearch(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        # Mock database connection and cursor
        self.db_patch = patch('DB.database_connection.DatabaseConnection')
        self.mock_db_connection = self.db_patch.start()
        self.mock_db = self.mock_db_connection().connect()
        self.mock_cursor = self.mock_db.cursor(dictionary=True)
        self.mock_cursor.fetchall.return_value = [{'id': 1, 'brand': 'Test', 'model': 'Model', 'year': 2020, 'price': 25000}]

    def tearDown(self):
        self.db_patch.stop()

    def test_validate_input_int(self):
        # Test valid integer input
        result = validate_input('123', 'int')
        self.assertEqual(result, 123)

        # Test invalid integer input
        with self.assertRaises(BadRequest):
            validate_input('abc', 'int')

    def test_validate_input_str(self):
        # Test valid string input
        result = validate_input('Test', 'str', 10)
        self.assertEqual(result, 'Test')

        # Test invalid string input with forbidden characters
        with self.assertRaises(BadRequest):
            validate_input('Test;Drop', 'str')

        # Test string too long
        with self.assertRaises(BadRequest):
            validate_input('ThisIsTooLongStringForTest', 'str', 10)

    def test_search_vehicles_valid(self):
        with self.client:
            with patch('flask.request') as mock_request:
                mock_request.args.get.side_effect = lambda x, default='': {
                    'brand': 'Test',
                    'model': 'Model',
                    'year_min': '2010',
                    'year_max': '2020',
                    'price_min': '20000',
                    'price_max': '30000',
                    'mileage_min': '5000',
                    'mileage_max': '10000'
                }[x]
                vehicles = search_vehicles()
                self.mock_cursor.execute.assert_called_once()
                self.assertIn('WHERE 1=1 AND brand LIKE %s AND model LIKE %s AND year >= %s AND year <= %s AND price >= %s AND price <= %s AND mileage >= %s AND mileage <= %s', self.mock_cursor.execute.call_args[0][0])

    def test_search_vehicles_invalid_input(self):
        with self.client:
            with patch('flask.request') as mock_request:
                mock_request.args.get.side_effect = lambda x, default='': {
                    'brand': 'Test;',
                    'model': '',
                    'year_min': 'not-a-year'
                }[x]
                with self.assertRaises(BadRequest):
                    search_vehicles()

if __name__ == '__main__':
    unittest.main()
