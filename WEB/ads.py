from flask import Blueprint, request, jsonify, current_app
from DB.database_connection import DatabaseConnection

ads_bp = Blueprint('ads', __name__)

db_instance = DatabaseConnection()

def get_db_connection():
    return db_instance.connect()

""" Vytvoří novou reklamu podle dat poskytnutých ve formátu JSON. """
@ads_bp.route('/ads', methods=['POST'])
def create_ad():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO ads (title, image_url, target_url, start_date, end_date, active) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (data['title'], data['image_url'], data['target_url'], data['start_date'], data['end_date'], data.get('active', True)))
        conn.commit()
        ad_id = cursor.lastrowid
        current_app.logger.info(f'New ad created with ID: {ad_id}')
        return jsonify(ad_id=ad_id), 201
    except Exception as e:
        current_app.logger.error(f'Error creating ad: {e}')
        return jsonify(message="Error creating ad"), 500
    finally:
        cursor.close()
        conn.close()

""" Získá všechny aktivní reklamy z databáze. """
@ads_bp.route('/ads', methods=['GET'])
def get_ads():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM ads WHERE active = TRUE"
        cursor.execute(query)
        ads = cursor.fetchall()
        current_app.logger.info('Fetched all active ads')
        return jsonify(ads)
    except Exception as e:
        current_app.logger.error(f'Error fetching ads: {e}')
        return jsonify(message="Error fetching ads"), 500
    finally:
        cursor.close()
        conn.close()

""" Aktualizuje existující reklamu podle ID a dat poskytnutých ve formátu JSON. """
@ads_bp.route('/ads/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE ads SET title=%s, image_url=%s, target_url=%s, start_date=%s, end_date=%s, active=%s WHERE ad_id=%s"
        cursor.execute(query, (data['title'], data['image_url'], data['target_url'], data['start_date'], data['end_date'], data['active'], ad_id))
        conn.commit()
        updated_rows = cursor.rowcount
        if updated_rows:
            current_app.logger.info(f'Ad {ad_id} updated')
        else:
            current_app.logger.warning(f'No ad found with ID {ad_id} to update')
        return jsonify(message="Ad updated")
    except Exception as e:
        current_app.logger.error(f'Error updating ad {ad_id}: {e}')
        return jsonify(message="Error updating ad"), 500
    finally:
        cursor.close()
        conn.close()

""" Smazání reklamy podle ID. """
@ads_bp.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM ads WHERE ad_id=%s"
        cursor.execute(query, (ad_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        if deleted_rows:
            current_app.logger.info(f'Ad {ad_id} deleted')
        else:
            current_app.logger.warning(f'No ad found with ID {ad_id} to delete')
        return jsonify(message="Ad deleted" if deleted_rows else "No ad found"), (200 if deleted_rows else 404)
    except Exception as e:
        current_app.logger.error(f'Error deleting ad {ad_id}: {e}')
        return jsonify(message="Error deleting ad"), 500
    finally:
        cursor.close()
        conn.close()