from flask import Blueprint, flash, redirect, url_for, session, current_app
from DB.database_connection import DatabaseConnection

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    admin_id = session.get('user_id', 'Unknown')  # Případ, že ID není dostupné
    if session.get('role') == 'admin':
        current_app.logger.info(f"Admin {admin_id} attempting to delete user {user_id}")
        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor()
        try:
            cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))
            db_connection.commit()
            flash('Uživatel byl úspěšně smazán.', 'success')
            current_app.logger.info(f"User {user_id} successfully deleted by admin {admin_id}")
        except Exception as e:
            db_connection.rollback()
            flash(f'Nastala chyba při smazání uživatele: {e}', 'danger')
            current_app.logger.error(f"Failed to delete user {user_id} by admin {admin_id}: {e}")
        finally:
            cursor.close()
            db_connection.close()
        return redirect(url_for('auth.page'))
    else:
        flash('Nemáte oprávnění pro tuto operaci.', 'danger')
        current_app.logger.warning(f"User {admin_id} unauthorized attempt to delete user {user_id}")
        return redirect(url_for('auth.login_view'))

@admin.route('/delete-vehicle/<int:vehicle_id>', methods=['POST'], endpoint='admin_delete_vehicle')
def delete_vehicle_admin(vehicle_id):
    admin_id = session.get('user_id', 'Unknown')
    if session.get('role') == 'admin':
        current_app.logger.info(f"Admin {admin_id} attempting to delete vehicle {vehicle_id}")
        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor()
        try:
            cursor.execute("DELETE FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
            db_connection.commit()
            flash('Vozidlo bylo úspěšně smazáno.', 'success')
            current_app.logger.info(f"Vehicle {vehicle_id} successfully deleted by admin {admin_id}")
        except Exception as e:
            db_connection.rollback()
            flash(f'Nastala chyba při smazání vozidla: {e}', 'danger')
            current_app.logger.error(f"Failed to delete vehicle {vehicle_id} by admin {admin_id}: {e}")
        finally:
            cursor.close()
            db_connection.close()
        return redirect(url_for('auth.page'))
    else:
        flash('Nemáte oprávnění pro tuto operaci.', 'danger')
        current_app.logger.warning(f"User {admin_id} unauthorized attempt to delete vehicle {vehicle_id}")
        return redirect(url_for('auth.login_view'))


# Testy pro adminfeatures.py
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_testing import TestCase

class TestAdminFeatures(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'secret'
        app.register_blueprint(admin)
        return app

    def setUp(self):
        self.db_patch = patch('DB.database_connection.DatabaseConnection')
        self.mock_db_connection = self.db_patch.start()
        self.mock_db = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_db_connection().connect.return_value = self.mock_db
        self.mock_db.cursor.return_value = self.mock_cursor

    def tearDown(self):
        self.db_patch.stop()

    def test_delete_user_admin(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['role'] = 'admin'
            response = self.client.post('/admin/delete-user/1')
            self.mock_cursor.execute.assert_called_once_with("DELETE FROM Users WHERE UserID = %s", (1,))
            self.assertRedirects(response, url_for('auth.page'))

    def test_delete_user_not_admin(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['role'] = 'user'
            response = self.client.post('/admin/delete-user/1')
            self.mock_cursor.execute.assert_not_called()
            self.assertRedirects(response, url_for('auth.login_view'))

    def test_delete_vehicle_admin(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['role'] = 'admin'
            response = self.client.post('/admin/delete-vehicle/1')
            self.mock_cursor.execute.assert_called_once_with("DELETE FROM Vehicles WHERE VehicleID = %s", (1,))
            self.assertRedirects(response, url_for('auth.page'))

    def test_delete_vehicle_not_admin(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['role'] = 'user'
            response = self.client.post('/admin/delete-vehicle/1')
            self.mock_cursor.execute.assert_not_called()
            self.assertRedirects(response, url_for('auth.login_view'))

if __name__ == '__main__':
    unittest.main()
