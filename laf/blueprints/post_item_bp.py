from flask import Blueprint, render_template, request, redirect, url_for, current_app
import mysql.connector
import os
from werkzeug.utils import secure_filename
from datetime import datetime

post_item_bp = Blueprint('post_item', __name__, template_folder='../templates')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lost_and_found'
    )
    return connection

@post_item_bp.route('/post_item', methods=['GET', 'POST'])
def post_item():
    success_message = None

    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        location = request.form['location']
        date_found = datetime.now().date()
        
        # Handle image file upload
        image_file = request.files['image']
        image_path = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)

            # Define the full path to save the file
            full_path = os.path.join(current_app.static_folder, 'uploads', filename)

            # Save the file to the uploads directory
            os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Ensure the directory exists
            image_file.save(full_path)

            image_path = filename  # Only store the filename in the database

        # Save data to the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO items (item_name, description, location, date_found, status, image_path) VALUES (%s, %s, %s, %s, %s, %s)",
            (item_name, description, location, date_found, 'pending', image_path)
        )
        connection.commit()
        cursor.close()
        connection.close()

        success_message = "Found Item Data successfully submitted. We'll review your submitted details first before publishing it to the public."

    return render_template('post_item.html', success_message=success_message)