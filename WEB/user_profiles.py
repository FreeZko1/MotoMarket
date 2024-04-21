from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from DB.database_connection import DatabaseConnection
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange

user_profiles = Blueprint('user_profiles', __name__)


@user_profiles.route('/profile/<int:user_id>')
def profile(user_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
        flash("Pro přístup k profilu se prosím přihlaste.", "info")
        return redirect(url_for('auth.login_view'))
    
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)

    # Získání informací o uživateli
    cursor.execute("SELECT UserID, FirstName, LastName, Email, AboutMe FROM Users WHERE UserID = %s", (user_id,))
    user_profile = cursor.fetchone()
    
    # Získání recenzí uživatele
    cursor.execute("SELECT r.*, u.FirstName as ReviewerFirstName, u.LastName as ReviewerLastName FROM Reviews r JOIN Users u ON r.author_id = u.UserID WHERE r.user_id = %s ORDER BY r.created_at DESC", (user_id,))
    reviews = cursor.fetchall()

    cursor.close()
    db_connection.close()

    if not user_profile:
        flash('Profil uživatele nebyl nalezen.', 'error')
        return redirect(url_for('user_profiles.list_profiles'))  # předpokládáme, že máte tuto routu

    return render_template('profile.html', user=user_profile, reviews=reviews, current_user_id=current_user_id)


@user_profiles.route('/add-review/<int:user_id>', methods=['POST'])
def add_review(user_id):
    if 'user_id' not in session:
        flash("Pro přidání recenze se musíte přihlásit.", "info")
        return redirect(url_for('auth.login_view'))

    content = request.form['content']
    rating = int(request.form['rating'])
    author_id = session['user_id']

    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO reviews (author_id, user_id, content, rating) VALUES (%s, %s, %s, %s)",
                   (author_id, user_id, content, rating))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    flash('Recenze byla úspěšně přidána.', 'success')
    # Redirect to the profile page of the user whose profile was reviewed
    return redirect(url_for('user_profiles.profile', user_id=user_id))




class ReviewForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10, max=500)])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Review')


import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, template_rendered
from werkzeug.exceptions import BadRequest

class UserProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'secret'
        self.app.register_blueprint(user_profiles)
        self.client = self.app.test_client()

        # Patch the database connection and cursor
        self.db_patch = patch('DB.database_connection.DatabaseConnection')
        self.mock_db_connection = self.db_patch.start()
        self.mock_db = self.mock_db_connection().connect()
        self.mock_cursor = self.mock_db.cursor(dictionary=True)

    def tearDown(self):
        self.db_patch.stop()

    def test_profile_not_logged_in(self):
        with self.client:
            response = self.client.get('/profile/1')
            self.assertEqual(response.status_code, 302)
            self.assertIn('auth.login_view', response.location)

    def test_profile_logged_in_but_no_profile(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['user_id'] = 1
            self.mock_cursor.fetchone.return_value = None
            response = self.client.get('/profile/1')
            self.assertEqual(response.status_code, 302)
            self.assertIn('user_profiles.list_profiles', response.location)

    def test_profile_success(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['user_id'] = 1
            self.mock_cursor.fetchone.side_effect = [
                {'UserID': 1, 'FirstName': 'John', 'LastName': 'Doe', 'Email': 'john@example.com', 'AboutMe': 'Hello'},
                [{'author_id': 1, 'content': 'Great user!', 'rating': 5}]
            ]
            response = self.client.get('/profile/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Hello', response.get_data(as_text=True))

    def test_add_review_not_logged_in(self):
        response = self.client.post('/add-review/1', data={'content': 'Great!', 'rating': 5})
        self.assertEqual(response.status_code, 302)
        self.assertIn('auth.login_view', response.location)

    def test_add_review_success(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['user_id'] = 2
            response = self.client.post('/add-review/1', data={'content': 'Great!', 'rating': 5}, follow_redirects=True)
            self.mock_cursor.execute.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertIn('Recenze byla úspěšně přidána.', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
