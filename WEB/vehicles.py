from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from DB.database_connection import DatabaseConnection
from flask import send_file
from flask import current_app
from werkzeug.utils import secure_filename

import io

# Vytvoření instance Blueprintu
vehicles = Blueprint('vehicles', __name__)

# Route pro zobrazení stránky s vozy
@vehicles.route('/home')
def home():
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT v.VehicleID, v.Brand, v.Model, v.YearOfManufacture, v.Mileage, v.Price, vi.ImageData FROM Vehicles v LEFT JOIN VehicleImages vi ON v.VehicleID = vi.VehicleID;")
        vehicles = cursor.fetchall()
        current_app.logger.info("Vehicle home page accessed successfully.")
    except Exception as e:
        current_app.logger.error(f"Failed to load vehicles: {e}")
        flash("Error loading vehicles", "error")
    finally:
        cursor.close()
        db_connection.close()
    if not vehicles:
        current_app.logger.info("No vehicles found in database.")
    return render_template('page.html', vehicles=vehicles)



@vehicles.route('/image/<int:vehicle_id>')
def serve_image(vehicle_id):
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor()
    cursor.execute("SELECT ImageData FROM VehicleImages WHERE VehicleID = %s", (vehicle_id,))
    image_data = cursor.fetchone()
    cursor.close()
    db_connection.close()
    if image_data and image_data[0]:
        print("Data found")  # Debugging
        return send_file(
            io.BytesIO(image_data[0]),
            mimetype='image/jpeg',
            as_attachment=False
        )
    else:
        print("No data found")  # Debugging
        return 'No image', 404





@vehicles.route('/add-vehicle', methods=['POST'])
def add_vehicle():
    if request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')
        year_of_manufacture = request.form.get('year')
        mileage = request.form.get('mileage')
        price = request.form.get('price')
        image = request.files.get('image')
        user_id = session.get('user_id')  # Předpokládá, že UserID je uložené v session

        if not (brand and model and year_of_manufacture and mileage and price and user_id):
            flash('Všechna pole musí být vyplněna.', 'danger')
            return redirect(url_for('vehicles.home'))

        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor()

        try:
            # Vložení vozidla do databáze
            cursor.execute("""
                INSERT INTO Vehicles (Brand, Model, YearOfManufacture, Mileage, Price, UserID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (brand, model, year_of_manufacture, mileage, price, user_id))
            db_connection.commit()

            # Získání ID nově vloženého vozidla
            vehicle_id = cursor.lastrowid

            # Zpracování a ukládání obrázku, pokud byl nahrán
            if image and image.filename:
                filename = secure_filename(image.filename)
                image_data = image.read()
                cursor.execute("""
                    INSERT INTO VehicleImages (VehicleID, ImageData)
                    VALUES (%s, %s)
                """, (vehicle_id, image_data))
                db_connection.commit()

            flash('Vozidlo bylo úspěšně přidáno.', 'success')
        except Exception as e:
            db_connection.rollback()
            flash(f'Nepodařilo se přidat vozidlo: {e}', 'danger')
        finally:
            cursor.close()
            db_connection.close()

        return redirect(url_for('vehicles.home'))



@vehicles.route('/delete-vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    if 'user_id' not in session:
        flash('Pro smazání inzerátu se prosím přihlaste.', 'danger')
        return redirect(url_for('auth.login_view'))

    user_id = session['user_id']
    role = session.get('role', 'user')

    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT UserID FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
        vehicle = cursor.fetchone()
        if vehicle and (user_id == vehicle['UserID'] or role == 'admin'):
            cursor.execute("DELETE FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
            db_connection.commit()
            current_app.logger.info(f"Vehicle {vehicle_id} deleted by user {user_id}")
            flash('Inzerát byl úspěšně smazán.', 'success')
        else:
            flash('Nemáte oprávnění k této akci.', 'danger')
            current_app.logger.warning(f"Unauthorized attempt to delete vehicle {vehicle_id} by user {user_id}")
    except Exception as e:
        db_connection.rollback()
        current_app.logger.error(f"Failed to delete vehicle {vehicle_id}: {e}")
        flash(f'Nastala chyba při smazání inzerátu: {e}', 'danger')
    finally:
        cursor.close()
        db_connection.close()

    return redirect(url_for('vehicles.home'))

from .search import search_vehicles

@vehicles.route('/search')
def search():
    return search_vehicles()

# Příklad přidání routy pro profil uživatele


@vehicles.route('/vehicle/<int:vehicle_id>')
def spec_vehicle(vehicle_id):
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    try:
        # Načtení informací o vozidle
        cursor.execute("""
            SELECT v.VehicleID, v.Brand, v.Model, v.YearOfManufacture, v.Mileage, v.Price, v.UserID, u.FirstName, u.LastName
            FROM Vehicles v
            LEFT JOIN Users u ON v.UserID = u.UserID
            WHERE v.VehicleID = %s
        """, (vehicle_id,))
        vehicle = cursor.fetchone()

                # Načtení historie vozidla
        cursor.execute("""
            SELECT h.Date, h.Description, h.Type, h.Cost, h.Document
            FROM VehicleHistory h
            WHERE h.VehicleID = %s
            ORDER BY h.Date DESC
        """, (vehicle_id,))
        history = cursor.fetchall()

        
        # Načtení recenzí vozidla
        cursor.execute("SELECT vr.*, u.FirstName as ReviewerFirstName, u.LastName as ReviewerLastName, vr.created_at FROM VehicleReviews vr JOIN Users u ON vr.author_id = u.UserID WHERE vr.vehicle_id = %s ORDER BY vr.created_at DESC", (vehicle_id,))
        vehicle_reviews = cursor.fetchall()
    finally:
        cursor.close()
        db_connection.close()

    if not vehicle:
        flash('Vozidlo nenalezeno', 'error')
        return redirect(url_for('vehicles.home'))

    return render_template('specvehicle.html', vehicle=vehicle, history=history, reviews=vehicle_reviews)








@vehicles.route('/add-history/<int:vehicle_id>', methods=['POST'])
def add_vehicle_history(vehicle_id):
    if 'user_id' not in session:
        flash("Pro přidání historie se musíte přihlásit.", "info")
        return redirect(url_for('auth.login_view'))

    description = request.form['description']
    date = request.form['date']
    type = request.form['type']
    cost = request.form['cost'] if 'cost' in request.form else None
    document = request.files.get('document')  # Upraveno z request.files['document'] na request.files.get('document')

    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor()

    # Kontrola, zda je soubor nahrán
    if document and document.filename:  # Přidáno: a dokument má název souboru
        document_filename = document.filename
    else:
        document_filename = None  # Pokud soubor není nahrán, nastavíme None

    try:
        cursor.execute("INSERT INTO VehicleHistory (VehicleID, Date, Description, Type, Cost, Document) VALUES (%s, %s, %s, %s, %s, %s)",
                       (vehicle_id, date, description, type, cost, document_filename))
        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        flash(f'Nastala chyba při přidávání historie: {e}', 'error')
    finally:
        cursor.close()
        db_connection.close()

    flash('Historie vozidla byla úspěšně přidána.', 'success')
    return redirect(url_for('vehicles.spec_vehicle', vehicle_id=vehicle_id))


@vehicles.route('/view-history/<int:vehicle_id>')
def view_vehicle_history(vehicle_id):
    
    print("Metoda view_vehicle_history byla zavolána")

    if 'user_id' not in session:
        flash("Pro zobrazení historie se musíte přihlásit.", "info")
        return redirect(url_for('auth.login_view'))

    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor()

    history = None
    try:
        cursor.execute("SELECT Date, Description, Type, Cost, Document FROM VehicleHistory WHERE VehicleID = %s", (vehicle_id,))
        history = cursor.fetchall()
        print(history)  # Tento řádek vypíše načtená data do konzole.
    except Exception as e:
        flash(f'Nastala chyba při načítání historie: {e}', 'error')
    finally:
        cursor.close()
        db_connection.close()

    if not history:
        flash('Pro toto vozidlo neexistuje žádná historie.', 'info')

    return render_template('view_history.html', history=history, vehicle_id=vehicle_id)


@vehicles.route('/vehicle/<int:vehicle_id>')
def vehicle_detail(vehicle_id):
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)

    # Získání detailů vozidla
    cursor.execute("SELECT * FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
    vehicle = cursor.fetchone()

    # Získání recenzí k vozidlu
    cursor.execute("SELECT r.*, u.FirstName, u.LastName FROM VehicleReviews r JOIN Users u ON r.author_id = u.UserID WHERE r.vehicle_id = %s ORDER BY r.created_at DESC", (vehicle_id,))
    vehicle_reviews = cursor.fetchall()

    cursor.close()
    db_connection.close()

    if not vehicle:
        flash('Vozidlo nenalezeno.', 'error')
        return redirect(url_for('vehicles.home'))

    return render_template('vehicle_detail.html', vehicle=vehicle, vehicle_reviews=vehicle_reviews)

@vehicles.route('/add-vehicle-review/<int:vehicle_id>', methods=['POST'])
def add_vehicle_review(vehicle_id):
    if 'user_id' not in session:
        flash("Pro přidání recenze se musíte přihlásit.", "info")
        return redirect(url_for('auth.login'))

    author_id = session['user_id']
    content = request.form['content']
    rating = request.form['rating']

    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor()
    try:
        # Přidání recenze do databáze
        cursor.execute("INSERT INTO VehicleReviews (vehicle_id, author_id, content, rating) VALUES (%s, %s, %s, %s)",
                       (vehicle_id, author_id, content, rating))
        db_connection.commit()
        flash('Vaše recenze byla úspěšně přidána.', 'success')
    except Exception as e:
        db_connection.rollback()
        flash(f'Nastala chyba při přidávání recenze: {e}', 'danger')
    finally:
        cursor.close()
        db_connection.close()

    return redirect(url_for('vehicles.vehicle_detail', vehicle_id=vehicle_id))
