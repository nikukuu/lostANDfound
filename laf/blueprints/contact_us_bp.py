from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector

contact_us_bp = Blueprint('contact_us', __name__, template_folder='../templates')

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lost_and_found'
    )
    return connection

@contact_us_bp.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    success_message = None

    if request.method == 'POST':
        # Retrieve form data
        item_id = request.form['item_id']
        claimer_name = request.form['claimer_name']
        contact_info = request.form['contact_info']
        message = request.form['message']

        # Validate inputs
        if not item_id.isdigit() or int(item_id) < 1:
            flash("Invalid Item ID. Must be a positive number.", 'danger')
            return render_template('contact_us.html')

        if len(claimer_name.strip()) == 0 or len(claimer_name) > 100:
            flash("Invalid Claimer Name. Must be 1-100 characters.", 'danger')
            return render_template('contact_us.html')

        if len(contact_info.strip()) == 0 or len(contact_info) > 150:
            flash("Invalid Contact Info. Must be 1-150 characters.", 'danger')
            return render_template('contact_us.html')

        if len(message) > 500:
            flash("Message too long. Max 500 characters.", 'danger')
            return render_template('contact_us.html')

        # Insert into database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO claims (item_id, claimer_name, contact_info, message) VALUES (%s, %s, %s, %s)",
            (item_id, claimer_name, contact_info, message)
        )
        connection.commit()
        cursor.close()
        connection.close()

        success_message = "Thank you! Your claim request has been submitted."

    return render_template('contact_us.html', success_message=success_message)