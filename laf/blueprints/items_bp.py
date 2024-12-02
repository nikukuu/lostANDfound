from flask import Blueprint, render_template, request
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

@items_bp.route('/items', methods=['GET'])
def items():
    query = request.args.get('query', '')  # Get the search query from the request
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if query:  # If there's a search query, filter items
        search_query = f"%{query}%"
        cursor.execute(
            "SELECT * FROM items WHERE status='published' AND (item_name LIKE %s OR description LIKE %s OR location LIKE %s)",
            (search_query, search_query, search_query)
        )
    else:  # No query, fetch all items
        cursor.execute("SELECT * FROM items WHERE status='published'")
    
    items = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('items.html', items=items)
