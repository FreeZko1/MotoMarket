from flask import Blueprint, render_template, request, jsonify, session, current_app, send_file, make_response
from DB.database_connection import DatabaseConnection
import io

compare = Blueprint('compare', __name__)

@compare.route('/compare-vehicles', methods=['GET'])
def compare_vehicles():
    current_app.logger.warning("metoda get vehicles se spustilaaaaa")

    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT VehicleID, Brand, Model, YearOfManufacture, Mileage, Price FROM Vehicles")
    vehicles = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return render_template('comparevehicle.html', vehicles=vehicles)

@compare.route('/api/compare', methods=['GET'])
def get_vehicles_api():
    current_app.logger.warning("metoda get vehicles se spustila")
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT VehicleID, Brand, Model, YearOfManufacture, Mileage, Price FROM Vehicles")
    vehicles = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return jsonify(vehicles)

@compare.route('/vehicle-image/<int:vehicle_id>')
def vehicle_image(vehicle_id):
    db_connection = DatabaseConnection().connect()
    cursor = db_connection.cursor(dictionary=True)  # Přidejte dictionary=True
    cursor.execute("SELECT ImageData FROM VehicleImages WHERE VehicleID = %s", (vehicle_id,))
    image_data = cursor.fetchone()

    cursor.close()
    db_connection.close()
    if image_data:
        return send_file(io.BytesIO(image_data['ImageData']), mimetype='image/jpeg')
    else:
        return "No image found", 404
    
# V modulu, kde máte definovaný Blueprint 'compare', přidejte tento endpoint
@compare.route('/select-vehicle', methods=['POST'])
def select_vehicle():
    vehicle_id = request.form.get('vehicle_id')
    if not vehicle_id:
        return jsonify({'status': 'error', 'message': 'No vehicle ID provided'}), 400

    if 'selected_vehicles' not in session:
        session['selected_vehicles'] = []

    if vehicle_id not in session['selected_vehicles']:
        session['selected_vehicles'].append(vehicle_id)
        # Log the updated session
        current_app.logger.warning(f"session: {session}")

        # Update the cookie manually (although Flask does this automatically)
        response = make_response(render_template('comparevehicle.html'))
        response.set_cookie('selected_vehicles', ','.join(session['selected_vehicles']))
        return response

    else:
        return jsonify({'status': 'error', 'message': 'Vehicle already selected'}), 400


@compare.route('/compare-selected-vehicles', methods=['GET'])
def compare_selected_vehicles():
    current_app.logger.warning("compare selected vehicles se volá")
    vehicle_ids = session.get('selected_vehicles', [])
    current_app.logger.warning(f"aaaa{vehicle_ids}")
    vehicles = []
    if vehicle_ids:
        db_connection = DatabaseConnection().connect()
        cursor = db_connection.cursor(dictionary=True)
        for vehicle_id in vehicle_ids:
            cursor.execute("SELECT * FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
            vehicle = cursor.fetchone()
            if vehicle:
                vehicles.append(vehicle)
                current_app.logger.warning(f"{vehicle} , {vehicles}")
        cursor.close()
        db_connection.close()
    return render_template('comparevehicle.html', vehicles=vehicles)



