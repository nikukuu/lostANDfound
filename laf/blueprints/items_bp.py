from flask import Blueprint, render_template
import mysql.connector

items_bp = Blueprint('items', __name__, template_folder='../templates')

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lost_and_found'
    )
    return connection

@items_bp.route('/items')
def items():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE status='published'")
    items = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('items.html', items=items)