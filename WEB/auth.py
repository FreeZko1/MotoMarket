from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from DB.database_connection import DatabaseConnection
import re
from WEB.news import get_news
from flask import current_app
from WEB.faq import faq_data  # Přizpůsobte cestu importu podle struktury vašeho projektu

auth = Blueprint("auth", __name__)


@auth.route("/")
def login_view():
    current_app.logger.info("Accessing the login page")
    return render_template("login.html")

# Přihlašovací funkce
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['loginEmail']
        password = request.form['loginPassword']

        current_app.logger.info(f"Attempt to login with email: {email}")

        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and user['Password'] == password:
            session['user_id'] = user['UserID']
            session['role'] = user['Role']
            current_app.logger.info(f"User {email} logged in successfully")
            return redirect(url_for('auth.page'))
        else:
            flash('Invalid login credentials.', 'danger')
            current_app.logger.warning(f"Login failed for {email}")

    return render_template("login.html", faq_data)




@auth.route("/register", methods=['GET', 'POST'])
def register():
    # Přednastavení hodnot
    username = ''
    firstName = ''
    lastName = ''
    email = ''
    password = ''
    phone = ''

    if request.method == 'POST':
        username = request.form.get('registerUsername', '')
        firstName = request.form.get('registerFirstName', '')
        lastName = request.form.get('registerLastName', '')
        email = request.form.get('registerEmail', '')
        password = request.form.get('registerPassword', '')
        phone = request.form.get('registerPhone', '')

        current_app.logger.info(f"Attempting to register user with username: {username}, email: {email}")

        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor(dictionary=True)
        valid = True

        # Ověření e-mailu, uživatelského jména, jména, příjmení, telefonního čísla a hesla
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Zadejte platnou e-mailovou adresu.', 'danger')
            valid = False
            current_app.logger.warning(f"Invalid email format provided: {email}")

        cursor.execute('SELECT * FROM Users WHERE username = %s', (username,))
        if cursor.fetchone():
            flash('Uživatelské jméno je již používáno.', 'danger')
            valid = False
            current_app.logger.warning(f"Username already in use: {username}")

        if not re.match(r"^[a-zA-ZěščřžýáíéďťňůúĚŠČŘŽÝÁÍÉĎŤŇŮÚ\s]{1,30}$", firstName + lastName):
            flash('Jméno a příjmení musí obsahovat pouze písmena a diakritiku a být kratší než 30 znaků.', 'danger')
            valid = False
            current_app.logger.warning(f"Invalid name format for user: {firstName} {lastName}")

        if not re.match(r"^\d{9}$", phone):
            flash('Telefonní číslo musí obsahovat přesně 9 čísel.', 'danger')
            valid = False
            current_app.logger.warning(f"Invalid phone format provided: {phone}")
        else:
            cursor.execute('SELECT * FROM Users WHERE PhoneNumber = %s', (phone,))
            if cursor.fetchone():
                flash('Telefonní číslo je již používáno.', 'danger')
                valid = False
                current_app.logger.warning(f"Phone number already in use: {phone}")

        if not re.match(r"^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{7,}$", password):
            flash('Heslo musí obsahovat minimálně jedno velké písmeno, jedno číslo a musí být delší než 6 znaků.', 'danger')
            valid = False
            current_app.logger.warning("Password does not meet the security requirements")

        if valid:
            try:
                cursor.execute('''INSERT INTO Users (username, FirstName, LastName, Email, Password, PhoneNumber, Role) 
                                  VALUES (%s, %s, %s, %s, %s, %s, 'User')''', 
                               (username, firstName, lastName, email, password, phone))
                db_connection.commit()
                flash('Registrace proběhla úspěšně. Nyní se můžete přihlásit.', 'success')
                current_app.logger.info(f"User registered successfully: {username}")
                return redirect(url_for('auth.login_view'))
            except Exception as e:
                flash(f'Nastala chyba při registraci: {e}', 'danger')
                db_connection.rollback()
                current_app.logger.error(f"Error during registration: {e}")
        else:
            return render_template("registration.html", username=username, firstName=firstName, lastName=lastName, email=email, password=password, phone=phone)

    return render_template("registration.html", username=username, firstName=firstName, lastName=lastName, email=email, password=password, phone=phone)


@auth.route("/page")
def page():
    current_app.logger.info("Accessing the main page with vehicle and news data")

    try:
        # Připojení k databázi
        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor(dictionary=True)
        
        # Načtení dat o vozidlech z databáze
        cursor.execute("SELECT v.VehicleID, v.Brand, v.Model, v.YearOfManufacture, v.Mileage, v.Price, vi.ImageData FROM Vehicles v LEFT JOIN VehicleImages vi ON v.VehicleID = vi.VehicleID")
        vehicles = cursor.fetchall()
        current_app.logger.info(f"Loaded {len(vehicles)} vehicles from the database")
        
        # Načtení novinek
        news_items = get_news()
        current_app.logger.info(f"Loaded news items")

        cursor.close()
        db_connection.close()
    except Exception as e:
        current_app.logger.error(f"Error accessing page data: {e}")
        flash("Nastala chyba při načítání dat.", "danger")
        vehicles = []
        news_items = []
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    # Předání dat do šablony
    return render_template("page.html", vehicles=vehicles, news_items=news_items, faq_data=faq_data)

@auth.route('/edit-profile', methods=['POST'])
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("Pro úpravu profilu se prosím přihlaste.", "info")
        current_app.logger.warning("Attempt to access profile edit without being logged in")
        return redirect(url_for('auth.login_view'))

    # Získání dat z formuláře
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    about_me = request.form.get('aboutMe', '')  # Bezpečně získáváme data, default je prázdný řetězec

    current_app.logger.info(f"User {user_id} is updating their profile")

    try:
        # Otevření databázového připojení
        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor()
        
        # Aktualizace databáze
        cursor.execute(
            "UPDATE Users SET FirstName=%s, LastName=%s, Email=%s, AboutMe=%s WHERE UserID=%s",
            (first_name, last_name, email, about_me, user_id)
        )
        db_connection.commit()
        flash("Informace o profilu byly aktualizovány.", "success")
        current_app.logger.info(f"Profile for user {user_id} was successfully updated")
    except Exception as e:
        db_connection.rollback()
        flash(f"Nastala chyba při aktualizaci profilu: {e}", "danger")
        current_app.logger.error(f"Error updating profile for user {user_id}: {e}")
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    return redirect(url_for('auth.profile'))

@auth.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("Pro přístup k profilu se prosím přihlaste.", "info")
        current_app.logger.warning("Attempt to access the profile page without logging in")
        return redirect(url_for('auth.login_view'))

    try:
        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor(dictionary=True)

        # Získání informací o uživateli
        cursor.execute("SELECT UserID, FirstName, LastName, Email, PhoneNumber, AboutMe FROM Users WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        current_app.logger.info(f"Profile data retrieved for user ID {user_id}")

        # Získání recenzí uživatele
        cursor.execute("SELECT r.*, u.FirstName as ReviewerFirstName, u.LastName as ReviewerLastName FROM Reviews r JOIN Users u ON r.author_id = u.UserID WHERE r.user_id = %s ORDER BY r.created_at DESC", (user_id,))
        reviews = cursor.fetchall()
        current_app.logger.info(f"User reviews loaded for user ID {user_id}")
    except Exception as e:
        current_app.logger.error(f"Error retrieving profile data for user ID {user_id}: {e}")
        flash("Nastala chyba při načítání dat profilu.", "danger")
        return redirect(url_for('auth.login_view'))
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

    if not user:
        flash("Uživatel nebyl nalezen.", "warning")
        current_app.logger.warning(f"No user found with ID {user_id}")
        return redirect(url_for('auth.login_view'))

    return render_template('profile.html', user=user, reviews=reviews, current_user_id=user_id)

from functools import wraps
from flask import session, redirect, url_for, flash

def requires_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            user_role = session.get('role')
            if 'user_id' not in session or ('role' not in session or session['role'] not in roles):
                current_app.logger.warning(f"Unauthorized access attempt by user {user_id} with role {user_role}")
                flash("Nemáte oprávnění k této operaci", "danger")
                return redirect(url_for('auth.login_view'))
            current_app.logger.info(f"User {user_id} with role {user_role} accessing {f.__name__}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth.route("/logout")
def logout():
    user_id = session.get('user_id', 'Unknown')  # Případ, že ID není dostupné
    current_app.logger.info(f"User {user_id} is logging out")
    session.clear()  # Odstraní všechny údaje uložené v session
    flash("Byli jste úspěšně odhlášeni.", "success")
    current_app.logger.info("Session cleared and user successfully logged out")
    return redirect(url_for('auth.login_view'))  # Přesměrování na přihlašovací stránku
