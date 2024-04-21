from flask import Blueprint, request, jsonify, render_template, session
import mysql.connector
from datetime import datetime
from DB.database_connection import DatabaseConnection
from flask import redirect
from flask import url_for
from flask import current_app



chat = Blueprint('chat', __name__)



def get_db_connection():
    # Tato funkce vytvoří nové spojení s databází
    return mysql.connector.connect(
        host="hostname",
        user="username",
        passwd="password",
        database="databasename"
    )

@chat.route('/chat-with/<int:recipient_id>')
def chat_page(recipient_id):
    user_id = session.get('user_id')
    if not user_id:
        current_app.logger.warning("Unauthenticated access attempt to chat page")
        return redirect(url_for('auth.login_view'))
    
    current_app.logger.info(f"User {user_id} accessing chat page with user {recipient_id}")
    return render_template('chat.html', recipient_id=recipient_id)

import mysql.connector
from DB.database_connection import DatabaseConnection

@chat.route('/api/send-message', methods=['POST'])
def send_message():
    sender_id = request.form.get('sender_id')
    recipient_id = request.form.get('recipient_id')
    text = request.form.get('text')

    if not sender_id or not recipient_id or not text:
        current_app.logger.warning("Failed message send attempt due to missing fields")
        return jsonify(success=False, message="Missing required fields"), 400

    db_connection = DatabaseConnection()  # Vytvoření instance
    db = db_connection.connect()  # Připojení k databázi
    try:
        cursor = db.cursor()
        query = """
        INSERT INTO ChatMessages (SenderUserID, RecipientUserID, MessageText, Timestamp)
        VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (sender_id, recipient_id, text))
        db.commit()
        current_app.logger.info(f"Message sent from user {sender_id} to {recipient_id}")
        return jsonify(success=True)
    except Exception as e:
        db.rollback()
        current_app.logger.error(f"Failed to send message from user {sender_id} to {recipient_id}: {e}")
        return jsonify(success=False, message=str(e)), 500
    finally:
        cursor.close()
        db.close()

@chat.route('/api/messages/<int:sender_id>/<int:recipient_id>', methods=['GET'])
def get_messages(sender_id, recipient_id):
    db_connection = DatabaseConnection()  # Vytvoření instance
    db = db_connection.connect()  # Připojení k databázi
    try:
        cursor = db.cursor(dictionary=True)
        query = """
        SELECT cm.MessageText, cm.Timestamp, u.FirstName, u.LastName 
        FROM ChatMessages cm
        JOIN Users u ON u.UserID = cm.SenderUserID
        WHERE (cm.SenderUserID = %s AND cm.RecipientUserID = %s)
        OR (cm.SenderUserID = %s AND cm.RecipientUserID = %s)
        ORDER BY cm.Timestamp ASC
        """
        cursor.execute(query, (sender_id, recipient_id, recipient_id, sender_id))
        messages = cursor.fetchall()
        current_app.logger.info(f"Retrieved messages between users {sender_id} and {recipient_id}")
        return jsonify(messages)
    except Exception as e:
        current_app.logger.error(f"Error retrieving messages between users {sender_id} and {recipient_id}: {e}")
        return jsonify(success=False, message=str(e)), 500
    finally:
        cursor.close()
        db.close()



@chat.route('/chat-list')
def chat_list():
    user_id = session.get('user_id')
    if not user_id:
        current_app.logger.warning("Unauthenticated access attempt to chat list")
        return redirect(url_for('auth.login_view'))

    db = DatabaseConnection.connect()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT DISTINCT u.UserID, u.FirstName, u.LastName FROM Users u
    JOIN ChatMessages cm ON cm.SenderUserID = u.UserID OR cm.RecipientUserID = u.UserID
    WHERE cm.SenderUserID = %s OR cm.RecipientUserID = %s;
    """
    cursor.execute(query, (user_id, user_id))
    chat_users = cursor.fetchall()
    current_app.logger.info(f"User {user_id} accessed chat list")
    cursor.close()
    db.close()
    return render_template('chat.html', chat_users=chat_users)


@chat.route('/api/chat-users/<int:user_id>', methods=['GET'])
def get_chat_users(user_id):
    current_app.logger.info(f"Retrieving chat users for user ID {user_id}")
    db_connection = DatabaseConnection()  # Vytvoření instance
    db = db_connection.connect()  # Připojení k databázi
    try:
        cursor = db.cursor(dictionary=True)
        query = """
        SELECT DISTINCT u.UserID, u.FirstName, u.LastName
        FROM ChatMessages cm
        JOIN Users u ON u.UserID = cm.SenderUserID OR u.UserID = cm.RecipientUserID
        WHERE (cm.SenderUserID = %s OR cm.RecipientUserID = %s) AND u.UserID != %s;
        """
        cursor.execute(query, (user_id, user_id, user_id))
        users = cursor.fetchall()
        current_app.logger.info(f"Found {len(users)} users associated with user ID {user_id}")
        return jsonify(users)
    except Exception as e:
        current_app.logger.error(f"Error retrieving chat users for user ID {user_id}: {e}")
        return jsonify(success=False, message=str(e)), 500
    finally:
        cursor.close()
        db.close()