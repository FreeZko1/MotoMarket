from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import json
from DB.database_connection import DatabaseConnection
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange
from flask import current_app


news = Blueprint('news', __name__)

class ApplicationForm(FlaskForm):
    first_name = StringField('Jméno', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Příjmení', validators=[DataRequired(), Length(min=2, max=50)])
    birth_number = StringField('Rodné číslo', validators=[DataRequired(), Regexp(r'^\d{6}/\d{3,4}$')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefonní číslo', validators=[DataRequired(), Regexp(r'^\+?\d{9,15}$')])
    age = IntegerField('Věk', validators=[DataRequired(), NumberRange(min=18)])
    city = StringField('Město bydliště', validators=[DataRequired(), Length(min=2, max=100)])
    postal_code = IntegerField('PSČ', validators=[DataRequired()])
    motivation = TextAreaField('Proč bys to chtěl/a dělat', validators=[DataRequired()])
    experience = TextAreaField('Zkušenosti', validators=[DataRequired()])
    years_experience = IntegerField('Roky zkušeností', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Odeslat')


@news.route('/submit-application', methods=['GET', 'POST'])
def submit_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        application_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'birth_number': form.birth_number.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'age': form.age.data,
            'city': form.city.data,
            'postal_code': form.postal_code.data,
            'motivation': form.motivation.data,
            'experience': form.experience.data,
            'years_experience': form.years_experience.data
        }

        current_app.logger.info(f"Application submitted: {application_data}")

        # Uložení dat do souboru JSON
        try:
            with open('staffForm.json', 'a') as f:
                json.dump(application_data, f, ensure_ascii=False, indent=4)
                f.write('\n')  # Přidá nový řádek po každém záznamu
            flash('Vaše žádost byla úspěšně odeslána a uložena.', 'success')
        except Exception as e:
            current_app.logger.error(f"Failed to save application data: {e}")
            flash(f'Chyba při ukládání aplikace: {e}', 'danger')

        return redirect(url_for('news.show_news'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f'{fieldName}: {err}', 'error')
                current_app.logger.warning(f"Validation error - {fieldName}: {err}")

    return render_template('apply.html', form=form)


@news.route('/news')
def show_news():
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT NewsID, Title, Description, ActionURL FROM News")
        news_items = cursor.fetchall()
        current_app.logger.info("News items successfully retrieved")
    except Exception as e:
        current_app.logger.error(f"Failed to retrieve news items: {e}")
        flash("Chyba při načítání novinek.", "danger")
    finally:
        cursor.close()
        db_connection.close()

    if not news_items:
        flash("Žádné novinky nebyly nalezeny.", "info")
        current_app.logger.warning("No news items found")

    return render_template('news.html', news_items=news_items)


def get_news():
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT Title, Description, ActionURL FROM News")
    news_items = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return news_items

def insert_news():
    news_items = [
        ('Hledáme admina', 'Naše stránka hledá nového administrátora. Pokud máte zájem, klikněte pro více informací.', 'url_kde_se_mohou_uchazeči_přihlásit'),
        ('Hledáme vývojáře', 'Přidejte se k našemu týmu jako vývojář. Klikněte zde pro podrobnosti a přihlášení.', 'url_kde_se_mohou_uchazeči_přihlásit')
    ]
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor()
    cursor.executemany("INSERT INTO News (Title, Description, ActionURL) VALUES (%s, %s, %s)", news_items)
    db_connection.commit()
    cursor.close()
    db_connection.close()

# Spusťte tuto funkci jednou, aby se data přidala do vaší databáze

@news.route('/form/<int:news_id>')
def show_form(news_id):
    form = ApplicationForm()
    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info(f"Form for news ID {news_id} submitted")
        return redirect(url_for('news.show_news'))
    current_app.logger.info(f"Displaying form for news ID {news_id}")
    return render_template('specific_form.html', news_id=news_id)


import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session, redirect, url_for
from flask_wtf import FlaskForm

class NewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.register_blueprint(news)
        self.client = self.app.test_client()

        # Patch the database connection and cursor
        self.db_patch = patch('DB.database_connection.DatabaseConnection')
        self.mock_db_connection = self.db_patch.start()
        self.mock_db = self.mock_db_connection().connect()
        self.mock_cursor = self.mock_db.cursor(dictionary=True)

    def tearDown(self):
        self.db_patch.stop()

    def test_show_news(self):
        # Simulate fetching news items
        self.mock_cursor.fetchall.return_value = [{'NewsID': 1, 'Title': 'Test News', 'Description': 'A test news item', 'ActionURL': 'http://example.com'}]
        response = self.client.get('/news')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test News', response.data)

    def test_submit_application_get(self):
        response = self.client.get('/submit-application')
        self.assertEqual(response.status_code, 200)

    def test_submit_application_post_valid(self):
        with self.client:
            self.mock_cursor.fetchall.return_value = []
            form_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'birth_number': '123456/1234',
                'email': 'test@example.com',
                'phone': '+123456789',
                'age': 25,
                'city': 'Prague',
                'postal_code': 12345,
                'motivation': 'I love this job',
                'experience': 'Lots of it',
                'years_experience': 5
            }
            response = self.client.post('/submit-application', data=form_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            # Použití Unicode stringu místo byte stringu
            self.assertIn('Vaše žádost byla úspěšně odeslána a uložena.', response.get_data(as_text=True))

    def test_get_news_function(self):
        # Simulate the `get_news` function's behavior
        self.mock_cursor.fetchall.return_value = [{'Title': 'Test News', 'Description': 'Description', 'ActionURL': 'http://example.com'}]
        news_items = get_news()
        self.assertEqual(len(news_items), 1)
        self.assertEqual(news_items[0]['Title'], 'Test News')

    def test_insert_news_function(self):
        with patch('news.mysql.connector.connect') as mocked_connect:
            mocked_connect.return_value = self.mock_db
            insert_news()
            self.mock_cursor.executemany.assert_called_once()
            self.mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()